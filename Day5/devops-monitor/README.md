# DevOps Monitoring Dashboard

API REST de surveillance de serveurs en temps reel, construite avec **FastAPI**, visualisee via un dashboard **Streamlit**, containerisee avec **Docker**, et avec un pipeline **CI GitHub Actions** complet.

---

## Architecture

```text
api/                  FastAPI (port 8000)
  GET  /health        Liveness probe
  GET  /metrics       CPU, memoire, disque (psutil)
  WS   /ws/metrics    Stream JSON toutes les secondes
  POST /servers       Enregistrer un serveur (API key)
  GET  /servers       Lister les serveurs + statut
  GET  /servers/{id}  Obtenir un serveur
  DELETE /servers/{id} Supprimer (API key)
  POST /servers/{id}/check Health check manuel

dashboard/            Streamlit (port 8501)
  Onglet Metriques    KPIs + graphique live (fenetre 60s)
  Onglet Serveurs     Tableau colore + formulaire
```

---

## Prerequis

- Python 3.11+
- Docker & Docker Compose
- Make

---

## Lancement rapide

```bash
# 1. Cloner le depot
git clone https://github.com/Amine92-cpu/Python-Course-M2.git
cd Python-Course-M2

# 2. Configurer les variables d'environnement
cp .env.example .env
# Editer .env et remplir API_KEY avec une valeur de votre choix

# 3. Demarrer la stack complete
make up

# 4. Acceder aux services
# API Swagger : http://localhost:8000/docs
# Dashboard   : http://localhost:8501
```

---

## Commandes disponibles

| Commande | Description |
|----------|-------------|
| `make install` | Installer les dependances Python |
| `make lint` | Lancer flake8 sur le code |
| `make test` | Lancer les tests unitaires (coverage >= 75%) |
| `make build` | Construire les images Docker localement |
| `make integration-test` | Lancer les tests d'integration contre Docker |
| `make up` | Demarrer la stack complete en arriere-plan |
| `make down` | Arreter et nettoyer les conteneurs |
| `make logs` | Suivre les logs des services |
| `make dev` | Lancer l'API en mode developpement local |

---

## Variables d'environnement

| Variable | Description | Defaut |
|----------|-------------|--------|
| `API_KEY` | Cle d'acces a l'API (header `X-API-Key`) | *(obligatoire)* |
| `API_BASE_URL` | URL de l'API vue par le dashboard | `http://api:8000` |

---

## Structure du projet

```text
devops-monitor/
├── api/
│   ├── __init__.py
│   ├── main.py          # App FastAPI, routes, WebSocket
│   ├── models.py        # Dataclass Server + schemas Pydantic
│   ├── auth.py          # Dependance API key
│   ├── metrics.py       # get_system_metrics() via psutil
│   ├── poller.py        # Boucle async de polling
│   └── Dockerfile       # Build multi-stage
├── dashboard/
│   ├── app.py           # Dashboard Streamlit
│   └── Dockerfile
├── tests/
│   ├── test_metrics.py  # Tests unitaires metriques
│   ├── test_routes.py   # Tests unitaires routes API
│   └── test_integration.py  # Tests d'integration
├── .github/
│   └── workflows/
│       └── ci.yml       # Pipeline CI: lint -> test -> build -> integration
├── docker-compose.yml
├── .dockerignore
├── .env.example
├── Makefile
├── requirements.txt
└── README.md
```

---

## Pipeline CI (GitHub Actions)

Le pipeline se declenche sur chaque `push` et `pull_request` vers `main` :

1. **Lint** — flake8 sur tout le code Python
2. **Unit Tests** — pytest avec couverture >= 75%
3. **Docker Build + Integration Tests** — construction des images et tests d'integration contre le conteneur

Aucune image n'est poussee vers un registry externe.
