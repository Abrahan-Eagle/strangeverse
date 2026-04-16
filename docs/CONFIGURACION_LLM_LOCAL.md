# Configuracion LLM local y Qwen (StrangeVerse)

Este documento describe como enlazar **StrangeVerse** (`/var/www/strangeverse` o tu clon) con:

- **Ollama** en la misma maquina (Gemma, Qwen local, etc.) — API compatible OpenAI.
- **Qwen en la nube** (Alibaba Dashscope), como en el `.env.example` oficial.
- **Dos LLM** (`LLM_*` + `LLM_BOOST_*`) en simulaciones paralelas del backend.

**No aplica:** modelos integrados en **Cursor CLI** (`composer-2-fast`, etc.): no exponen un HTTP API estilo OpenAI para que el backend de StrangeVerse los llame.

---

## Donde lee el `.env` el backend

El archivo debe estar en la **raiz del repo StrangeVerse** (junto a `package.json`), no dentro de `backend/`.

La carga esta en `backend/app/config.py` (`load_dotenv` sobre `../../.env`).

---

## Variables obligatorias (arranque `python run.py`)

| Variable | Uso |
|----------|-----|
| `LLM_API_KEY` | **No puede estar vacia** (`Config.validate()`). Para Ollama suele bastar un valor dummy no vacio, p. ej. `ollama`. |
| `LLM_BASE_URL` | Base URL API compatible OpenAI (termina en `/v1` para muchos proveedores). |
| `LLM_MODEL_NAME` | Nombre del modelo tal como lo lista el servidor (Ollama: `ollama list`). |
| `ZEP_API_KEY` | **Obligatoria** para arrancar el servidor Flask. El proyecto usa [Zep Cloud](https://app.getzep.com/) para memoria/grafo; no hay flag upstream para desactivarla sin tocar codigo. |

---

## Perfil A — Ollama (Gemma, Qwen local, etc.)

1. Instala [Ollama](https://ollama.com/) y descarga el modelo, p. ej. `ollama pull gemma3:4b` (ajusta el nombre a tu caso).
2. Comprueba que responde la API compatible OpenAI (puerto por defecto **11434**):

```bash
curl -sS http://127.0.0.1:11434/v1/models
```

3. En `.env` (raiz StrangeVerse):

```env
LLM_API_KEY=ollama
LLM_BASE_URL=http://127.0.0.1:11434/v1
LLM_MODEL_NAME=gemma3:4b
```

Sustituye `LLM_MODEL_NAME` por el nombre exacto de `ollama list`.

**Notas:** Los modelos locales pueden quedarse cortos en contexto o calidad frente a simulaciones largas; el README upstream recomienda empezar con **pocas rondas** de simulacion. El consumo es principalmente **CPU/GPU local**, no facturacion de API (salvo Zep).

---

## Perfil B — Qwen en la nube (Dashscope)

Alineado con `.env.example` del repo:

```env
LLM_API_KEY=tu_clave_dashscope
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL_NAME=qwen-plus
```

Obtener clave y detalles en la consola Alibaba / Bailian (Dashscope).

---

## Perfil C — `LLM` principal + `LLM_BOOST` (simulacion paralela)

En `backend/scripts/run_parallel_simulation.py`, la funcion `create_model(..., use_boost=True)` usa **LLM_BOOST_*** cuando esta definido `LLM_BOOST_API_KEY` (no vacio). Asi se pueden repartir **dos proveedores** (p. ej. uno local y uno en la nube) para **mas concurrencia** en simulaciones paralelas.

Ejemplo: principal Ollama, secundario Dashscope:

```env
# Principal (paralelo "general")
LLM_API_KEY=ollama
LLM_BASE_URL=http://127.0.0.1:11434/v1
LLM_MODEL_NAME=gemma3:4b

# Boost (cuando el script usa use_boost y hay boost configurado)
LLM_BOOST_API_KEY=tu_clave_dashscope
LLM_BOOST_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_BOOST_MODEL_NAME=qwen-plus
```

Si **no** vas a usar boost, **no** definas las variables `LLM_BOOST_*` (ni siquiera vacias con nombres presentes), para evitar confusion.

El servidor Flask principal (`run.py`) usa **solo** `LLM_*` de `Config`, no el bloque boost.

---

## Zep (`ZEP_API_KEY`)

Registrate en Zep, crea una API key y ponla en:

```env
ZEP_API_KEY=tu_clave_zep
```

Sin esto, `Config.validate()` falla al arrancar el backend.

---

## Comprobacion rapida del endpoint LLM

### Con el script incluido

Desde la raiz del repo StrangeVerse:

```bash
chmod +x scripts/check-llm-endpoint.sh
./scripts/check-llm-endpoint.sh
```

Lee `LLM_BASE_URL` y `LLM_API_KEY` del `.env` y hace una peticion `GET .../models` (API compatible OpenAI).

### Manual con curl

Sustituye la URL si tu `LLM_BASE_URL` es distinta:

```bash
curl -sS -H "Authorization: Bearer ollama" http://127.0.0.1:11434/v1/models
```

Para Dashscope, usa tu `LLM_API_KEY` real en la cabecera si el proveedor lo exige.

---

## Otras variables utiles (opcional)

| Variable | Descripcion |
|----------|-------------|
| `OASIS_DEFAULT_MAX_ROUNDS` | Rondas por defecto (ej. `10`). Subir mucho aumenta llamadas al LLM. |
| `FLASK_HOST` / `FLASK_PORT` | Host y puerto del backend (por defecto `5001`). |

---

## Si `POST /api/graph/ontology/generate` devuelve 500

Suele ser el LLM **sin JSON valido** (prosa, markdown, respuesta truncada) o **contenido vacio** en `content` con modelos tipo Gemma que envian texto a `reasoning`.

1. Cambia en `.env` a **`LLM_MODEL_NAME=qwen2.5:3b`** (u otro modelo que respete `response_format` JSON en Ollama).
2. Reinicia el backend (`npm run dev` o solo el proceso Python).
3. El codigo en `backend/app/utils/llm_client.py` intenta extraer el primer objeto JSON del texto si el modelo no devuelve solo JSON.

---

## Archivos relacionados

- Plantillas comentadas por perfil: [.env.profiles.example](../.env.profiles.example)
- Ejemplo minimo upstream: [.env.example](../.env.example)
