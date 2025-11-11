# CRUD FastAPI - Docker

## Requisitos
- Docker
- Docker Compose
- (Opcional) Python para ejecutar localmente

## Pasos
1. Copia `.env.example` a `.env` y ajusta credenciales.
2. Levantar containers:
   docker compose up --build -d
3. Comprobar logs:
   docker compose logs -f backend
4. Endpoints:
   GET  /health
   POST /products
   GET  /products
   GET  /products/{id}
   PUT  /products/{id}
   DELETE /products/{id}
