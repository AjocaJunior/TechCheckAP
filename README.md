# TechCheck Activity Provider

## Executar localmente

```bash
python -m venv .venv
# Linux/Mac:
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate

pip install -r requirements.txt
python app.py
```

Servidor: `http://localhost:8000`

## Endpoints
- GET  /
- GET  /config
- GET  /config/params
- POST /deploy
- GET  /analytics/list
- GET  /analytics
