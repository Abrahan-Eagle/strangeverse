<div align="center">

<img src="./static/image/strangeverse_logo_compressed.jpeg" alt="Logotipo de StrangeVerse" width="75%"/>

Motor de inteligencia colectiva conciso y universal — predice cualquier escenario
</br>
<em>StrangeVerse — simulación multiagente y grafos de escenarios</em>

<a href="https://www.shanda.com/" target="_blank"><img src="./static/image/shanda_logo.png" alt="Shanda" height="40"/></a>

[![Estrellas de GitHub](https://img.shields.io/github/stars/Abrahan-Eagle/strangeverse?style=flat-square&color=DAA520)](https://github.com/Abrahan-Eagle/strangeverse/stargazers)
[![Observadores de GitHub](https://img.shields.io/github/watchers/Abrahan-Eagle/strangeverse?style=flat-square)](https://github.com/Abrahan-Eagle/strangeverse/watchers)
[![GitHub Forks](https://img.shields.io/github/forks/Abrahan-Eagle/strangeverse?style=flat-square)](https://github.com/Abrahan-Eagle/strangeverse/network)
[![Docker](https://img.shields.io/badge/Docker-GHCR-2496ED?style=flat-square&logo=docker&logoColor=white)](https://github.com/Abrahan-Eagle/strangeverse/pkgs/container/strangeverse)

[![Discord](https://img.shields.io/badge/Discord-Join-5865F2?style=flat-square&logo=discord&logoColor=white)](http://discord.gg/ePf5aPaHnA)

[English](./README.md) | [Español](./README-ES.md)

</div>

## ⚡ Descripción general

**StrangeVerse** es un motor de predicción de IA de próxima generación impulsado por tecnología de múltiples agentes. Al extraer información inicial del mundo real (como noticias de última hora, borradores de políticas o señales financieras), construye automáticamente un mundo digital paralelo de alta fidelidad. Dentro de este espacio, miles de agentes inteligentes con personalidades independientes, memoria a largo plazo y lógica de comportamiento interactúan libremente y experimentan una evolución social. Puede inyectar variables dinámicamente desde una "vista de Dios" para deducir con precisión trayectorias futuras: **ensayar el futuro en un entorno de pruebas digital y tomar decisiones después de innumerables simulaciones**.

> Solo necesita: Cargar materiales iniciales (informes de análisis de datos o historias novedosas interesantes) y describir sus requisitos de predicción en lenguaje natural</br>
> StrangeVerse regresará: un informe de predicción detallado y un mundo digital de alta fidelidad profundamente interactivo

### Nuestra Visión

StrangeVerse se dedica a crear un espejo de inteligencia de enjambre que mapea la realidad. Al capturar el surgimiento colectivo desencadenado por interacciones individuales, superamos las limitaciones de la predicción tradicional:

- **A Nivel Macro**: Somos un laboratorio de ensayo para tomadores de decisiones, permitiendo probar políticas y relaciones públicas sin riesgo
- **A nivel micro**: somos un entorno de pruebas creativo para usuarios individuales: ya sea deduciendo finales novedosos o explorando escenarios imaginativos, todo puede ser divertido, divertido y accesible.

Desde predicciones serias hasta simulaciones divertidas, dejamos que cada "qué pasaría si" vea su resultado, haciendo posible predecir cualquier cosa.

## 🌐 Demostración en vivo

Ejecute la pila localmente (consulte **Inicio rápido** a continuación) o con Docker para obtener una experiencia completa. Es posible que más adelante se publique una demostración alojada públicamente desde este repositorio.
## 📸 Capturas de pantalla

<div align="center">
<tabla>
<tr>
<td><img src="./static/image/Screenshot/运行截图1.png" alt="Captura de pantalla 1" width="100%"/></td>
<td><img src="./static/image/Screenshot/运行截图2.png" alt="Captura de pantalla 2" width="100%"/></td>
</tr>
<tr>
<td><img src="./static/image/Screenshot/运行截图3.png" alt="Captura de pantalla 3" width="100%"/></td>
<td><img src="./static/image/Screenshot/运行截图4.png" alt="Captura de pantalla 4" width="100%"/></td>
</tr>
<tr>
<td><img src="./static/image/Screenshot/运行截图5.png" alt="Captura de pantalla 5" width="100%"/></td>
<td><img src="./static/image/Screenshot/运行截图6.png" alt="Captura de pantalla 6" width="100%"/></td>
</tr>
</tabla>
</div>

## 🎬 Vídeos de demostración

### 1. Simulación de opinión pública de la Universidad de Wuhan + Introducción al proyecto StrangeVerse

<div align="center">
<a href="https://www.bilibili.com/video/BV1VYBsBHEMY/" target="_blank"><img src="./static/image/武大模拟演示封面.png" alt="Video de demostración de StrangeVerse" width="75%"/></a>

Haga clic en la imagen para ver el vídeo de demostración completo para realizar predicciones utilizando el "Informe de opinión pública de la Universidad de Wuhan" generado por BettaFish.
</div>

### 2. Simulación del final perdido del Sueño de la Cámara Roja

<div align="center">
<a href="https://www.bilibili.com/video/BV1cPk3BBExq" target="_blank"><img src="./static/image/红楼梦模拟推演封面.jpg" alt="Video de demostración de StrangeVerse" width="75%"/></a>

Haga clic en la imagen para ver la profunda predicción de StrangeVerse sobre el final perdido basada en cientos de miles de palabras de los primeros 80 capítulos de "Dream of the Red Chamber".
</div>

> **Predicción financiera**, **Predicción de noticias políticas** y más ejemplos próximamente...

## 🔄 Flujo de trabajo
1. **Construcción de gráficos**: extracción de semillas e inyección de memoria individual/colectiva y construcción de GraphRAG
2. **Configuración del entorno**: extracción de relación de entidad, generación de persona e inyección de configuración de agente
3. **Simulación**: simulación paralela de plataforma dual, requisitos de predicción de análisis automático y actualizaciones dinámicas de memoria temporal
4. **Generación de informes**: ReportAgent con un rico conjunto de herramientas para una interacción profunda con el entorno posterior a la simulación
5. **Interacción profunda**: chatee con cualquier agente en el mundo simulado e interactúe con ReportAgent

## 🚀 Inicio rápido

### Opción 1: Implementación del código fuente (recomendado)

#### Requisitos previos

| Herramienta | Versión | Descripción | Verificar instalación |
|------|---------|-------------|-------------------|
| **Nodo.js** | 18+ | Tiempo de ejecución frontend, incluye npm | `nodo -v` |
| **Python** | ≥3,11, ≤3,12 | Tiempo de ejecución de back-end | `python --versión` |
| **uv** | Lo último | Administrador de paquetes de Python | `uv --versión` |

#### 1. Configurar variables de entorno

```golpecito
# Copiar el archivo de configuración de ejemplo
cp .env.ejemplo .env

# Edite el archivo .env y complete las claves API requeridas
```

**Variables de entorno requeridas:**

```entorno
# Configuración de API de LLM (admite cualquier API de LLM con formato OpenAI SDK)
# Recomendado: modelo Alibaba Qwen-plus a través de la plataforma Bailian: https://bailian.console.aliyun.com/
# Alto consumo, prueba primero simulaciones con menos de 40 rondas
LLM_API_KEY=tu_clave_api
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL_NAME=qwen-plus

# Configuración de la nube Zep
# La cuota mensual gratuita es suficiente para un uso sencillo: https://app.getzep.com/
ZEP_API_KEY=tu_zep_api_key
```
#### 2. Instalar dependencias

```golpecito
# Instalación con un clic de todas las dependencias (root + frontend + backend)
configuración de ejecución de npm: todo
```

O instalar paso a paso:

```golpecito
# Instalar dependencias de nodo (raíz + interfaz)
configuración de ejecución npm

# Instalar dependencias de Python (backend, crea automáticamente un entorno virtual)
configuración de ejecución de npm: backend
```

#### 3. Iniciar servicios

```golpecito
# Iniciar tanto el frontend como el backend (ejecutar desde la raíz del proyecto)
npm ejecutar desarrollador
```

**URL de servicio:**
- Interfaz: `http://localhost:3000`
- API de back-end: `http://localhost:5001`

**Comience individualmente:**

```golpecito
npm run backend # Iniciar solo el backend
npm run frontend # Iniciar solo la interfaz
```

### Opción 2: Implementación de Docker

```golpecito
# 1. Configurar variables de entorno (igual que la implementación de origen)
cp .env.ejemplo .env
# 2. Extraiga la imagen y comience
ventana acoplable componer -d
```

Lee `.env` desde el directorio raíz de forma predeterminada, asigna los puertos `3000 (frontend) / 5001 (backend)`

> La dirección reflejada para una extracción más rápida se proporciona como comentarios en `docker-compose.yml`, reemplácela si es necesario.

## 📬 Únase a la conversación

<div align="center">
<img src="./static/image/QQ群.png" alt="Grupo QQ" width="60%"/>
</div>

&nbsp;

Se aceptan comentarios y contribuciones a través de [GitHub Issues](https://github.com/Abrahan-Eagle/strangeverse/issues).

## 📄 Agradecimientos

**¡StrangeVerse ha recibido apoyo estratégico e incubación de Shanda Group!**

El motor de simulación de StrangeVerse funciona con **[OASIS (Open Agent Social Interaction Simulators)](https://github.com/camel-ai/oasis)**. ¡Agradecemos sinceramente al equipo de CAMEL-AI por sus contribuciones de código abierto!

## 📈 Estadísticas del proyecto

<a href="https://www.star-history.com/#Abrahan-Eagle/strangeverse&type=date&legend=top-left">
   <imagen>
   <source media="(prefiere-color-scheme: oscuro)" srcset="https://api.star-history.com/svg?repos=Abrahan-Eagle/strangeverse&type=date&theme=dark&legend=top-left" />
   <fuente media="(prefiere-color-esquema: claro)" srcset="https://api.star-history.com/svg?repos=Abrahan-Eagle/strangeverse&type=date&legend=top-left" />
   <img alt="Gráfico histórico de estrellas" src="https://api.star-history.com/svg?repos=Abrahan-Eagle/strangeverse&type=date&legend=top-left" />
 </imagen>
</a>