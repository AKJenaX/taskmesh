# TaskMesh

TaskMesh is a minimal full-stack task scheduling demo built for hackathon speed.

## Structure

```text
taskmesh/
├── backend/
│   ├── app.py
│   ├── routes.py
│   ├── schemas.py
│   ├── config.yaml
│   └── scheduler/
│       ├── core.py
│       ├── baseline.py
│       ├── env.py
│       └── utils.py
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── style.css
├── scripts/
│   ├── train.py
│   └── benchmark.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Run Backend

```bash
pip install -r requirements.txt
uvicorn backend.app:app --reload
```

The API will be available at `http://localhost:8000`.

## Run Frontend

Open `frontend/index.html` in a browser after starting the backend.

## API

- `GET /health`
- `POST /schedule`

Example payload:

```json
{
  "tasks": [
    {
      "id": "task-1",
      "title": "Demo review",
      "priority": 5,
      "duration_minutes": 30,
      "metadata": {}
    }
  ]
}
```
