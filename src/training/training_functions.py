from sklearn.model_selection import train_test_split
import pandas as pd
from typing import Tuple


class TrainingClass:
    """
    Clase para preparar datasets para entrenamiento, validación y prueba,
    y aplicar imputación por cuantiles para valores atípicos.

    Métodos:
        train_test_val(for_train_df: pd.DataFrame) ->
        Tuple[pd.DataFrame, pd.DataFrame,
        pd.DataFrame, pd.Series, pd.Series, pd.Series]:
            Divide el DataFrame en conjuntos
            de entrenamiento, validación y prueba.

        quantile_inputation(X_train: pd.DataFrame,
        X_test: pd.DataFrame, X_val: pd.DataFrame, column: str) ->
        Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
            Aplica recorte (clipping)
            de valores extremos basados en
            cuantiles 5% y 95% a una columna.

        training_dataframes() ->
        Tuple[pd.DataFrame, pd.DataFrame,
        pd.DataFrame, pd.Series, pd.Series, pd.Series]:
            Ejecuta el flujo completo de
            preparación de datos y retorna
            los conjuntos listos para entrenamiento.
    """

    def __init__(self, dataframe: pd.DataFrame) -> None:
        """
        Inicializa la clase con el DataFrame a procesar.

        Args:
            dataframe (pd.DataFrame):
            DataFrame que contiene los datos completos.
        """
        self.dataframe = dataframe

    def train_test_val(
        self, for_train_df: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame,
               pd.DataFrame, pd.Series,
               pd.Series, pd.Series]:
        """
        Divide el DataFrame en
        conjuntos de entrenamiento (70%), validación (15%) y prueba (15%).

        Args:
            for_train_df (pd.DataFrame):
            DataFrame con las variables de entrada y objetivo.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame,
            pd.DataFrame, pd.Series, pd.Series, pd.Series]:
                Conjuntos X_train, X_val, X_test, y_val, y_test, y_train.
        """
        X_train, X_temp, y_train, y_temp = train_test_split(
            for_train_df.drop('Target_90Days', axis=1),
            for_train_df['Target_90Days'],
            test_size=0.3,
            random_state=1
        )

        X_val, X_test, y_val, y_test = train_test_split(
            X_temp,
            y_temp,
            test_size=0.5,
            random_state=1
        )

        return X_train, X_val, X_test, y_val, y_test, y_train

    def quantile_inputation(
        self,
        X_train: pd.DataFrame,
        X_test: pd.DataFrame,
        X_val: pd.DataFrame,
        column: str
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Aplica clipping para
        limitar valores extremos en la columna especificada
        usando el percentil 5% como límite inferior y 95% como límite superior.

        Args:
            X_train (pd.DataFrame): Conjunto de entrenamiento.
            X_test (pd.DataFrame): Conjunto de prueba.
            X_val (pd.DataFrame): Conjunto de validación.
            column (str): Nombre de la columna a tratar.

        Returns:
            Tuple[pd.DataFrame,
            pd.DataFrame, pd.DataFrame]:
            Los tres conjuntos con la columna recortada.
        """
        lower_limit = X_train[column].quantile(0.05)
        upper_limit = X_train[column].quantile(0.95)

        X_train[column].clip(lower=lower_limit,
                             upper=upper_limit, inplace=True)
        X_test[column].clip(lower=lower_limit,
                            upper=upper_limit, inplace=True)
        X_val[column].clip(lower=lower_limit,
                           upper=upper_limit, inplace=True)

        return X_train, X_test, X_val

    def training_dataframes(
        self
    ) -> Tuple[pd.DataFrame, pd.DataFrame,
               pd.DataFrame, pd.Series, pd.Series, pd.Series]:
        """
        Ejecuta el flujo completo de preparación de datos para entrenamiento:
        - Divide el DataFrame en conjuntos train, val y test.
        - Aplica imputación por cuantiles en las columnas especificadas.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame,
            pd.DataFrame, pd.Series, pd.Series, pd.Series]:
                Conjuntos X_train, X_val,
                X_test, y_val, y_test, y_train listos para entrenamiento.
        """
        for_train_df = self.dataframe.copy()

        (X_train, X_val,
         X_test, y_val, y_test,
         y_train) = self.train_test_val(for_train_df)
        columns = ['Quantity', 'total']

        for column in columns:
            (X_train,
             X_val, X_test) = self.quantile_inputation(X_train,
                                                       X_test, X_val, column)

        return X_train, X_val, X_test, y_val, y_test, y_train
