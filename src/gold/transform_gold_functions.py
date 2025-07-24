import pandas as pd
import numpy as np


class GoldClass:
    """
    Clase para procesar y transformar
    datos en la etapa Gold del pipeline Medallion.

    Métodos:
        grouping(df: pd.DataFrame) -> pd.DataFrame:
            Agrupa los datos por
            CustomerID y DateColumn, agregando métricas de interés.

        creating_target(grouped_df: pd.DataFrame) -> pd.DataFrame:
            Crea la variable objetivo
            Target_90Days indicando si el cliente repite compra en 90 días,
            y genera la columna regroup_country codificada.

        all_gold_functions() -> pd.DataFrame:
            Ejecuta el flujo completo
            de agrupación y creación de target sobre el DataFrame inicial.
    """

    def __init__(self, dataframe: pd.DataFrame) -> None:
        """
        Inicializa la clase con un DataFrame.

        Args:
            dataframe (pd.DataFrame):
            DataFrame inicial con datos a transformar.
        """
        self.dataframe = dataframe

    def grouping(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Agrupa el DataFrame por 'CustomerID' y
        'DateColumn', sumando cantidades y totales,
        y seleccionando el primer país asociado.

        Args:
            df (pd.DataFrame): DataFrame a agrupar.

        Returns:
            pd.DataFrame: DataFrame agrupado y ordenado.
        """
        grouped_df = (
            df.groupby(["CustomerID", "DateColumn"])
            .agg(
                {
                    "Quantity": "sum",
                    "total_price_per_item": "sum",
                    "Country": "first",
                }
            )
            .reset_index()
        )

        # Filtrar CustomerID no nulos o distintos de "0"
        grouped_df = grouped_df[grouped_df["CustomerID"] != "0"]
        grouped_df.rename({"total_price_per_item":
                           "total"}, axis=1, inplace=True)
        grouped_df["DateColumn"] = pd.to_datetime(
            grouped_df["DateColumn"], format="%d-%m-%Y")
        grouped_df = grouped_df.sort_values(["CustomerID", "DateColumn"])

        return grouped_df

    def creating_target(self, grouped_df: pd.DataFrame) -> pd.DataFrame:
        """
        Crea la variable objetivo
        'Target_90Days' indicando si la siguiente compra del cliente
        ocurre dentro de los próximos
        90 días. Además, genera una columna binaria 'regroup_country'
        codificando 'United Kingdom' como 1 y otros como 0.

        Args:
            grouped_df (pd.DataFrame):
            DataFrame agrupado con datos de compras por cliente y fecha.

        Returns:
            pd.DataFrame: DataFrame con columnas para entrenamiento.
        """
        grouped_df["NextPurchaseDate"] = grouped_df.groupby(
            "CustomerID")["DateColumn"].shift(-1)
        grouped_df["days_since_last_purchase"] = (
            grouped_df["NextPurchaseDate"] - grouped_df["DateColumn"]).dt.days
        grouped_df["days_since_last_purchase"].fillna(-1, inplace=True)
        grouped_df[
            "days_since_last_purchase"] = grouped_df[
                "days_since_last_purchase"].astype(int)

        grouped_df["Target_90Days"] = np.where(
            (grouped_df["days_since_last_purchase"] <= 90) & (
                grouped_df["days_since_last_purchase"] != -1),
            1,
            0,
        )

        for_train_df = grouped_df[[
            "Quantity", "total", "Target_90Days", "Country"]].copy()

        # Crear columna agrupada para país
        for_train_df["regroup_country"] = np.where(
            for_train_df["Country"] == "United Kingdom",
            "United Kingdom",
            "other"
        )

        for_train_df.drop("Country", axis=1, inplace=True)

        # Codificar como binario
        for_train_df["regroup_country"] = np.where(
            for_train_df["regroup_country"] == "United Kingdom", 1, 0
        )

        return for_train_df

    def all_gold_functions(self) -> pd.DataFrame:
        """
        Ejecuta el pipeline
        completo de la etapa Gold: agrupación y creación de target.

        Returns:
            pd.DataFrame:
            DataFrame listo para entrenamiento con variables relevantes.
        """
        df = self.dataframe
        grouped_df = self.grouping(df)
        for_train_df = self.creating_target(grouped_df)

        return for_train_df
