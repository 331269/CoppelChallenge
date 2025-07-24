from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from silver.transform_silver_functions import SilverClass
from gold.transform_gold_functions import GoldClass
import numpy as np
from joblib import load
import uvicorn
from fastapi.responses import RedirectResponse
from typing import List, Optional
import sqlite3

app = FastAPI()


def load_model():
    return load('model.pkl')


loaded_model = load_model()


# Definir el modelo de entrada
class Data(BaseModel):
    InvoiceNo: str
    StockCode: str
    Description: str
    Quantity: int
    InvoiceDate: str
    UnitPrice: float
    CustomerID: Optional[float]
    Country: str


@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/docs")


@app.post("/predict/")
def receive_data(data: List[Data]):
    # Convertir lista de Data a DataFrame

    conn = sqlite3.connect('coppelchallenge.db')

    # Crear cursor para ejecutar queries
    # cursor = conn.cursor()

    df = pd.DataFrame([item.dict() for item in data])
    df.to_sql('ventas_bronze', conn, if_exists='append', index=False)

    # No reasignar columnas, ya vienen bien con item.dict()

    # Transformación Silver
    sil_class = SilverClass(df)
    df_silver = sil_class.all_functions()
    df_silver.to_sql('ventas_silver', conn, if_exists='append', index=False)

    # Transformación Gold
    gold_class = GoldClass(df_silver)
    df_gold = gold_class.grouping(df_silver)

    # Preparación para predicción
    for_train_df = df_gold[['Quantity', 'total', 'Country']].copy()

    # Renombrar columna 'Country' a 'regroup_country'
    for_train_df.rename(columns={'Country': 'regroup_country'}, inplace=True)

    # Verificar que exista 'regroup_country'
    if 'regroup_country' in for_train_df.columns:
        for_train_df['regroup_country'] = np.where(
            for_train_df['regroup_country'] == 'United Kingdom', 1, 0)
    else:
        return {"error": "No"
                "se encontró la columna 'regroup_country' en df_gold"}

    # Realizar predicción
    predictions = loaded_model.predict(for_train_df)

    for_train_df['predictions'] = predictions
    for_train_df.to_sql('outputs_table', conn, if_exists='append', index=False)
    print('outputs sent')

    return {
        "prediction": predictions.tolist()
    }


if __name__ == "__main__":

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
