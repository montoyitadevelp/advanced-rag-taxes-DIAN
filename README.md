# Advanced RAG System for DIAN Documents with FastAPI & PostgreSQL & OpenAI & React & Vite

Welcome to the Retrieval-Augmented Generation (RAG) system designed specifically for question answering on **DIAN's legal and tax documentation**. This is a **technical test** implementation that integrates OpenAI models, FastAPI, PostgreSQL and an architecture based on modern backend engineering principles like SOLID, dependency injection, and async support.

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-1.0-teal?logo=fastapi)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-4B00B5?logo=openai)](https://platform.openai.com/)
[![SwaggerUI](https://img.shields.io/badge/Swagger-UI-orange?logo=swagger)](https://swagger.io/tools/swagger-ui/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue?logo=postgresql)](https://www.postgresql.org/)
[![React](https://img.shields.io/badge/React-18.x-blue?logo=react)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/Vite-5.x-purple?logo=vite)](https://vitejs.dev/)

---

## 🧠 What is RAG?

**Retrieval-Augmented Generation (RAG)** combines a retriever (vector search) with a generator (LLM) to answer questions grounded on a specific corpus — in this case, **DIAN documents** involving **tax and legal regulations**. This system uses:

- `text-embedding-3-small` to vectorize content.
- `gpt-4o-mini` for answer generation.
- `heapq.nlargest` algorithm for semantic retrieval.
- FastAPI for serving endpoints.
- PostgreSQL for database

---

## 📸 System Architecture

### RAG Flow Diagram

![RAG Flow](/resources/img/Architecture_RAG.jpg)


### Project UML

![UML](/resources/img/UML.png)

### Create .env in the root directory

```text
DB_USER=postgres
DB_PASSWORD=CvaD12345
DB_NAME=postgres
```

## 🚀 Getting Started with Docker

### Prerequisites
- Docker desktop installed

### Clone the repository

```bash
git clone https://github.com/montoyitadevelp/advanced-rag-taxes-DIAN.git
cd advanced-rag-taxes-DIAN
```

### Create a `.env` file in the root directory

```plainttext
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_database_name
```

### Create a `.env` file in the `backend` directory

```plaintext
# Database
DB_USER="postgres"
DB_PASSWORD="password"
DB_HOST="localhost"
DB_NAME="postgres"
DB_PORT="5432"

# General
APP_NAME = Rag Taxes DIAN
FRONTEND_BASE_URL=http://localhost:5173/ 

# Security
BACKEND_CORS_ORIGIN='["http://localhost:5173", "http://localhost:5173/*"]'

# OpenAI
OPENAI_API_KEY="your_openai_api_key"
OPENAI_MODEL="gpt-4o"
OPENAI_EMBEDDING_MODEL="text-embedding-3-small"
PROMPT_TEMPLATE="Eres un asistente experto en materia tributaria y legal. Con base únicamente en la información proporcionada a continuación, responde de forma clara, precisa y profesional. Si no cuentas con suficiente información para responder, indícalo con transparencia. {context}\n\n---\n\nPregunta:\n{question}\n\n---\n\nRespuesta:"
```

### Create a `.env` file in the `frontend` directory

```plaintext
VITE_API_URL=http://localhost:8000/api/v1
```

### Start the Docker containers

```bash
docker-compose up --build
```

### Access the application
- **Frontend**: Open your browser and go to [http://localhost:5173](http://localhost:5173)
- **Backend**: Open your browser and go to [http://localhost:8000/docs](http://localhost:8000/docs) to access the Swagger UI.

### Stop the Docker containers
```bash
docker-compose down
```
### Start again the Docker containers
```bash
docker-compose up
```