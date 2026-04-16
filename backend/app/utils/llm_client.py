"""
LLM客户端封装
统一使用OpenAI格式调用
"""

import json
import logging
import re
from typing import Optional, Dict, Any, List, Union
from openai import OpenAI

from ..config import Config

logger = logging.getLogger(__name__)


def _first_json_object_from_text(text: str) -> Optional[Union[Dict[str, Any], List[Any]]]:
    """
    Algunos modelos locales (p. ej. Gemma via Ollama) devuelven prosa o JSON dentro de markdown
    en lugar de un unico objeto JSON. Intenta extraer el primer objeto JSON valido.
    """
    if not text or not text.strip():
        return None
    text = text.strip()
    # Bloque ```json ... ```
    m = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, flags=re.IGNORECASE)
    if m:
        chunk = m.group(1).strip()
        try:
            return json.loads(chunk)
        except json.JSONDecodeError:
            pass
    start = text.find("{")
    if start == -1:
        return None
    decoder = json.JSONDecoder()
    try:
        obj, _ = decoder.raw_decode(text[start:])
        return obj
    except json.JSONDecodeError:
        return None


class LLMClient:
    """LLM客户端"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None
    ):
        self.api_key = api_key or Config.LLM_API_KEY
        self.base_url = base_url or Config.LLM_BASE_URL
        self.model = model or Config.LLM_MODEL_NAME
        
        if not self.api_key:
            raise ValueError("LLM_API_KEY 未配置")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        response_format: Optional[Dict] = None
    ) -> str:
        """
        发送聊天请求
        
        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大token数
            response_format: 响应格式（如JSON模式）
            
        Returns:
            模型响应文本
        """
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        if response_format:
            kwargs["response_format"] = response_format
        
        response = self.client.chat.completions.create(**kwargs)
        msg = response.choices[0].message
        raw = msg.content if msg.content is not None else ""
        if not str(raw).strip():
            extra = getattr(msg, "model_extra", None) or {}
            if isinstance(extra, dict) and extra.get("reasoning"):
                raw = str(extra["reasoning"])
        # 部分模型（如MiniMax M2.5）会在content中包含<redacted_thinking>思考内容，需要移除
        content = re.sub(r'<redacted_thinking>[\s\S]*?</think>', '', str(raw)).strip()
        return content
    
    def chat_json(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 4096
    ) -> Dict[str, Any]:
        """
        发送聊天请求并返回JSON
        
        Args:
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大token数
            
        Returns:
            解析后的JSON对象
        """
        response = self.chat(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"}
        )
        # 清理markdown代码块标记
        cleaned_response = response.strip()
        cleaned_response = re.sub(r'^```(?:json)?\s*\n?', '', cleaned_response, flags=re.IGNORECASE)
        cleaned_response = re.sub(r'\n?```\s*$', '', cleaned_response)
        cleaned_response = cleaned_response.strip()

        try:
            return json.loads(cleaned_response)
        except json.JSONDecodeError:
            pass

        extracted = _first_json_object_from_text(cleaned_response)
        if isinstance(extracted, dict):
            logger.warning("chat_json: JSON parseado desde subcadena / markdown (modelo no devolvio solo JSON)")
            return extracted

        preview = (cleaned_response[:800] + "…") if len(cleaned_response) > 800 else cleaned_response
        raise ValueError(f"LLM返回的JSON格式无效: {preview}")
