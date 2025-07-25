# 🛍️ CoppelChallenge

Bienvenidos al proyecto del Challenge de Coppel, en este repositorio encontrarás toda la infraestructura del código, esto engloba el procesamiento del ETL para generar los datos crudos (bronze), filtrados (silver) y preparados para el entrenamiento del modelo de Machine Learning (gold). Así mismo, encontrarás el código con el cual se construye una API, la cual se explica más adelante.
En cada Pull Request se llevan a cabo GitHub Actions los cuales contemplan Linting, Testing, Build de Docker y SonarCloud. Además, la documentación de todo el proyecto se realiza usando Sphinx.

---

## ⚙️ Arquitectura del Proyecto

- **Bronze Layer**: Carga e ingesta de datos crudos desde CSV a SQLite (`ventas_bronze`).
- **Silver Layer**: Limpieza, validación y filtro de datos (`ventas_silver`).
- **Gold Layer**: Feature engineering y creación de la variable objetivo `Target_90Days` (`ventas_gold`) la cual representa el valor 1 (el cliente volverá dentro de los próximos 90 días) y 0 (el cliente no regresará).

---

## 🤖 Entrenamiento del Modelo

Durante el entrenamiento del modelo se toman en cuenta tres posibles modelos:

- Clasificación binaria: `RandomForest`, `GradientBoosting` y `XGBoost`.

Una vez entrenados los tres modelos se selecciona el que mejor performance tenga en su precision. La razón por la cual se escogió el precision como principal métrica es debido a la naturaleza del problema: para el negocio no es bueno predecir que alguien volverá a comprar en los próximos 90 días y que en realidad no lo haga.
Finalmente el modelo seleccionado se guarda como un `model.pkl`.

---

## 🧪 API REST (FastAPI)

### Endpoint `/predict/`  
Recibe datos de transacciones, aplica los filtros hechos en bronze y silver para alimentar el modelo. El output final son las predicciones del modelo más las variables 'Quantity', 'total', 'regroup_country', 'predictions', 'CustomerID' y 'fecha_procesamiento' con formato json:

La ingesta de datos sigue los siguientes pasos:
```1. ingresar datos como json en el POST /predict/
```
* Ejemplo:

📥 Entrada:
```json
[
  {
    "InvoiceNo": "536365",
    "StockCode": "85123A",
    "Quantity": 6,
    "UnitPrice": 2.55,
    "InvoiceDate": "12/1/2010 8:26",
    "CustomerID": 17850.0,
    "Country": "United Kingdom",
    "Description": "WHITE HANGING HEART T-LIGHT HOLDER"
  }
]
```

📤 Salida:
```json
{
  "data": [
    {
      "Quantity": 6,
      "total": 15.3,
      "regroup_country": 1,
      "predictions": 0,
      "CustomerID": "17850",
      "fecha_procesamiento": "2025-07-25T14:03:51.123Z"
    }
  ]
}



```
Cabe destacar, que cada vez que se hace ingresan datos, se llevan a cabo los siguientes filtros:
- Filtro de CustomerID nulo.
- Filtro de todos los registros que en la columna InvoiceNo que empiecen con "C".
- Creación de la columna "regroup_country" a partir de la columna "Country", donde 1 es para United Kingdom y 0 es para cualquier otro país.
---

## 🐳 Docker

La API corre completamente en Docker: cada vez que se haga un Pull Request, se lleva a cabo un Build de Docker.

### Complementos:

```bash
docker-compose up --build
```

Para usar el contenedor debe tomar en cuenta la siguiente línea:

"docker run -d -v "$(pwd)/model.pkl:/app/model.pkl" -p 8000:8000 coppelchallenge"

Ya que la imagen no se crea usando el modelo.
Una vez que corre la línea anterior, la API estará disponible en el siguiente link:

```
http://localhost:8000/docs
```

---

## 🧪 Tests

En cada PR se llevan a cabo los unit_test de la API y las funciones que usa (SilverClass y GoldClass)

```bash
pytest src/unit_test/
```

---

## 🗂️ Estructura General

```
src/
├── bronze/        # Ingesta de datos crudos
├── silver/        # Transformaciones de limpieza
├── gold/          # Feature engineering y creación de target
├── complete_medallion/   # invocación de todas las funciones de bronze, silver y gold
├── training/      # Entrenamiento de modelos
├── app.py         # API FastAPI
├── main.py        # Orquestador del pipeline completo
```

---

## 📄 Requisitos

Instalación de dependencias:

```bash
pip install -r requirements.txt
```

---

## 📌 Notas Finales

- Base de datos local: `coppelchallenge.db`
- Modelo entrenado guardado como `model.pkl`
- Cada vez que se usa la API se genera un logging
---
