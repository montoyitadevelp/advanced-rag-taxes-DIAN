## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/rag-backend-dian.git
cd rag-backend-dian
```
### 2. Create a virtual environment

```bash
python -m venv venv
```
### 3. Activate the virtual environment
- On Windows:

```bash
venv\Scripts\activate
```
- On macOS/Linux:

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Activate PYTHONPATH (optional)
```
cd backend
$env:PYTHONPATH = "$env:PYTHONPATH;$(Get-Location)"
```

### 6. Create a `.env` file
Create a `.env` file in the `backend` directory with the following content:

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
### 7. Run migrations

```bash
alembic upgrade head
```

### 8. Start the server

```bash
cd backend/src
uvicorn main:app --reload
```

### 9. Access the API docs
Open your browser and go to:

```
http://localhost:8000/docs
```

### 10. Access the general actions to the API
Open your browser and go to:

```
http://localhost:8000/api/v1

```