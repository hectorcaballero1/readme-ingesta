# readme-ingesta

Cuatro contenedores Python que extraen datos de los microservicios de ReadMe vía los endpoints `/api/export/`, convierten el JSON a CSV y suben los archivos a S3.

## Configuración

```bash
cp .env.example .env
```

Rellenar `.env`:

| Variable | Descripción |
|----------|-------------|
| `MS1_URL` | URL base de MS1 (ej. `http://1.2.3.4:8001`) |
| `MS2_URL` | URL base de MS2 (ej. `http://1.2.3.4:8002`) |
| `MS3_URL` | URL base de MS3 (ej. `http://1.2.3.4:8003`) |
| `MS6_URL` | URL base de MS6 (ej. `http://1.2.3.4:8006`) |
| `ADMIN_KEY` | Clave compartida de los microservicios |
| `AWS_ACCESS_KEY_ID` | Credencial AWS |
| `AWS_SECRET_ACCESS_KEY` | Credencial AWS |
| `AWS_REGION` | Región del bucket de analytics (ej. `us-east-1`) |
| `ANALYTICS_BUCKET` | Bucket S3 de analytics (distinto al bucket de fotos) |

## Ejecutar

```bash
docker compose up --build
```

Cada contenedor corre, sube sus CSVs y termina. Los cuatro corren en paralelo.

## Archivos generados en S3

| Contenedor | Archivo en S3 | Fuente |
|------------|---------------|--------|
| ingesta01 | `ms1/users.csv` | GET /api/export/users |
| ingesta01 | `ms1/zones.csv` | GET /api/export/zones |
| ingesta02 | `ms2/books.csv` | GET /api/export/books |
| ingesta02 | `ms2/categories.csv` | GET /api/export/categories |
| ingesta03 | `ms3/solicitudes.csv` | GET /api/export/solicitudes |
| ingesta06 | `ms6/transactions.csv` | GET /api/export/transactions |
| ingesta06 | `ms6/reviews.csv` | GET /api/export/reviews |

> En `ms3/solicitudes.csv` el campo `messages` se serializa como string JSON dentro de su columna.
