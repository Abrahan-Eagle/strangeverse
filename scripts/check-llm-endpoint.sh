#!/usr/bin/env bash
# Comprueba que el endpoint OpenAI-compatible responde (GET .../models).
# Uso: desde la raiz del repo StrangeVerse: ./scripts/check-llm-endpoint.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="${ROOT}/.env"

if [[ ! -f "${ENV_FILE}" ]]; then
  echo "No existe ${ENV_FILE}. Copia .env.example o .env.profiles.example y rellena valores." >&2
  exit 1
fi

set -a
# shellcheck disable=SC1090
source "${ENV_FILE}"
set +a

BASE="${LLM_BASE_URL:-}"
KEY="${LLM_API_KEY:-}"

if [[ -z "${BASE}" ]]; then
  echo "LLM_BASE_URL no definido en .env" >&2
  exit 1
fi

if [[ -z "${KEY}" ]]; then
  echo "LLM_API_KEY no definido en .env (usa un valor no vacio, p. ej. ollama para Ollama)" >&2
  exit 1
fi

URL="${BASE%/}/models"
echo "GET ${URL}"
HTTP_CODE="$(curl -sS -o /tmp/strangeverse-models-$$.json -w "%{http_code}" \
  -H "Authorization: Bearer ${KEY}" \
  "${URL}" || echo "000")"

echo "HTTP ${HTTP_CODE}"
if [[ "${HTTP_CODE}" == "200" ]]; then
  head -c 1200 /tmp/strangeverse-models-$$.json
  echo
  rm -f "/tmp/strangeverse-models-$$.json"
  exit 0
fi

cat /tmp/strangeverse-models-$$.json 2>/dev/null || true
rm -f "/tmp/strangeverse-models-$$.json"
exit 1
