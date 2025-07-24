from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import precision_score
from xgboost import XGBClassifier
import joblib
import pandas as pd
from typing import Any


def trainer(
    X_train: pd.DataFrame,
    X_val: pd.DataFrame,
    X_test: pd.DataFrame,
    y_val: pd.Series,
    y_test: pd.Series,
    y_train: pd.Series
) -> Any:
    """
    Entrena y evalúa varios modelos
    de clasificación, elige el mejor basado en precisión
    sobre el conjunto de validación,
    evalúa en el conjunto de prueba, guarda y retorna
    el modelo con mejor desempeño.

    Args:
        X_train (pd.DataFrame): Datos de entrenamiento (features).
        X_val (pd.DataFrame): Datos de validación (features).
        X_test (pd.DataFrame): Datos de prueba (features).
        y_val (pd.Series): Etiquetas de validación.
        y_test (pd.Series): Etiquetas de prueba.
        y_train (pd.Series): Etiquetas de entrenamiento.

    Returns:
        Any: El pipeline del modelo
        entrenado con mejor precisión
        (RandomForest, GradientBoosting o XGBoost).
    """
    counts = y_train.value_counts()

    # Calcular coeficiente para balancear clases en XGBClassifier
    coeff = counts[1] / counts[0]

    models = [
        RandomForestClassifier(),
        GradientBoostingClassifier(),
        XGBClassifier(scale_pos_weight=coeff)
    ]

    models_names = ['random', 'gradient', 'xgb']

    models_scores = {}
    models_trained = {}

    for name, model in zip(models_names, models):
        pipeline_model = Pipeline([
            ('standard', StandardScaler()),
            (name, model)
        ])

        pipeline_model.fit(X_train, y_train)
        y_pred = pipeline_model.predict(X_val)
        precision = precision_score(y_val, y_pred, zero_division=0)

        models_scores[name] = precision
        models_trained[name] = pipeline_model

    max_precision_model = max(models_scores, key=models_scores.get)
    final_pred = models_trained[max_precision_model].predict(X_test)
    final_precision = precision_score(y_test, final_pred, zero_division=0)
    print(
        "Final test precision of best model"
        f"({max_precision_model}): {final_precision}")

    joblib.dump(models_trained[max_precision_model], 'model.pkl')

    return models_trained[max_precision_model]
