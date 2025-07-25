from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from silver.transform_silver_functions import SilverClass
from gold.transform_gold_functions import GoldClass
import numpy as np
from joblib import load
import uvicorn
from fastapi.responses import RedirectResponse
from typing import List, Optional, Dict, Any
import sqlite3
import os
import logging
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("loggings"),  # guarda en archivo
        logging.StreamHandler()               # sigue mostrando en terminal
    ]
)

logger = logging.getLogger(__name__)

with open("quantiles.json", "r") as f:
    quan = json.load(f)

lower_quantity = quan['Quantity_lower']
upper_quantity = quan['Quantity_upper']
lower_total = quan['total_lower']
upper_total = quan['total_upper']

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_model() -> Any:
    """
    Carga el modelo previamente entrenado desde un archivo .pkl.

    Returns:
        Modelo cargado con joblib.load.
    """
    model_path = os.path.join(BASE_DIR, 'model.pkl')
    return load(model_path)


loaded_model = load_model()


class Data(BaseModel):
    """
    Modelo Pydantic para validar y tipar la entrada JSON al endpoint /predict/.
    """
    InvoiceNo: str
    StockCode: str
    Description: str
    Quantity: int
    InvoiceDate: str
    UnitPrice: float
    CustomerID: Optional[float]
    Country: str


@app.get("/", include_in_schema=False)
def redirect_to_docs() -> RedirectResponse:
    """
    Redirecciona la raíz '/' a la documentación automática Swagger UI.
    """
    return RedirectResponse(url="/docs")


@app.post("/predict/")
def receive_data(data: List[Data]) -> Dict[str, Any]:
    """
    Recibe una lista de objetos Data, los procesa y genera predicciones.

    Flujo:
    - Convierte la lista en DataFrame.
    - Inserta datos en tabla 'ventas_bronze'.
    - Aplica transformaciones Silver y guarda en 'ventas_silver'.
    - Aplica transformaciones Gold.
    - Prepara DataFrame para predicción.
    - Realiza predicción con el modelo cargado.
    - Guarda resultados en 'outputs_table'.
    - Retorna el DataFrame resultante en formato JSON.

    Args:
        data (List[Data]): Lista de objetos con la información de ventas.

    Returns:
        Dict[str, Any]: Diccionario con
        clave "data" y valor lista de registros con predicciones.
    """
    logger.info("Datos recibidos para predicción")
    conn = sqlite3.connect('coppelchallenge.db')

    # Convertir lista de Pydantic models a DataFrame
    df = pd.DataFrame([item.dict() for item in data])

    # Guardar datos crudos en tabla Bronze
    df.to_sql('ventas_bronze', conn, if_exists='append', index=False)

    # Transformación Silver y guardado
    sil_class = SilverClass(df)
    df_silver = sil_class.all_functions()
    df_silver.to_sql('ventas_silver', conn, if_exists='append', index=False)

    # Transformación Gold
    gold_class = GoldClass(df_silver)
    df_gold = gold_class.grouping(df_silver)

    # Preparar dataframe para predicción
    for_train_df = df_gold[['Quantity',
                            'total', 'Country', 'CustomerID']].copy()
    for_train_df.set_index('CustomerID', inplace=True)
    for_train_df.rename(columns={'Country': 'regroup_country'}, inplace=True)

    if 'regroup_country' in for_train_df.columns:
        for_train_df['regroup_country'] = np.where(
            for_train_df['regroup_country'] == 'United Kingdom', 1, 0)
    else:
        return {"error": "No se encontró la"
                "columna 'regroup_country' en df_gold"}

    for_train_df['Quantity'].clip(lower=lower_quantity,
                                  upper=upper_quantity, inplace=True)
    for_train_df['total'].clip(lower=lower_total,
                               upper=upper_total, inplace=True)

    # Predicción
    predictions = loaded_model.predict(for_train_df)
    for_train_df['predictions'] = predictions
    for_train_df.reset_index(inplace=True)

    # Ajustar tipo CustomerID y agregar fecha procesamiento
    for_train_df['CustomerID'] = for_train_df[
        'CustomerID'].astype(int).astype(str)
    for_train_df['fecha_procesamiento'] = pd.Timestamp.now()

    # Seleccionar columnas finales y guardar resultados
    for_train_df = for_train_df[['Quantity', 'total',
                                 'regroup_country', 'predictions',
                                 'CustomerID', 'fecha_procesamiento']]
    for_train_df.to_sql('outputs_table', conn, if_exists='append', index=False)

    print('outputs sent')

    return {
        "data": for_train_df.to_dict(orient="records")
    }


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
