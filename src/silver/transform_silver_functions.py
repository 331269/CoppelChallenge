import pandas as pd


class SilverClass:
    """
    Clase para realizar
    transformaciones de la capa Silver en el pipeline Medallion.
    Aplica limpieza, manejo de valores nulos, formateo de fechas
    y filtrado de datos.

    Métodos:
        handling_customer_na(df: pd.DataFrame) -> pd.DataFrame:
            Rellena valores nulos en 'CustomerID' y convierte a str.

        handling_time(df: pd.DataFrame) -> pd.DataFrame:
            Convierte 'InvoiceDate' a datetime y crea columna
            'DateColumn' con formato 'dd-mm-yyyy'.

        filtering(df: pd.DataFrame) -> pd.DataFrame:
            Filtra filas no deseadas según condiciones en
            'InvoiceNo', 'Quantity' y 'UnitPrice'.

        all_functions() -> pd.DataFrame:
            Aplica todas las transformaciones en orden y
            calcula el precio total por ítem.
    """

    def __init__(self, dataframe: pd.DataFrame) -> None:
        """
        Inicializa la clase con un DataFrame.

        Args:
            dataframe (pd.DataFrame): DataFrame original para transformar.
        """
        self.dataframe = dataframe

    def handling_customer_na(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Rellena los valores nulos en 'CustomerID'
        con 0 y convierte la columna a string.

        Args:
            df (pd.DataFrame): DataFrame a procesar.

        Returns:
            pd.DataFrame: DataFrame con 'CustomerID' limpio y tipo string.
        """
        df['CustomerID'] = df['CustomerID'].fillna(0)
        df['CustomerID'] = df['CustomerID'].astype('int').astype('str')
        return df

    def handling_time(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Convierte la columna 'InvoiceDate'
        a datetime y crea una columna 'DateColumn'
        con formato de fecha 'dd-mm-yyyy' como string.

        Args:
            df (pd.DataFrame): DataFrame a procesar.

        Returns:
            pd.DataFrame: DataFrame con columna
            'InvoiceDate' datetime y 'DateColumn' string.
        """
        df['InvoiceDate'] = pd.to_datetime(
            df['InvoiceDate'], format='%m/%d/%Y %H:%M')
        df['DateColumn'] = df['InvoiceDate'].dt.strftime('%d-%m-%Y')
        return df

    def filtering(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filtra filas del DataFrame eliminando:
            - Filas donde 'InvoiceNo'
            comienza con 'C' (devoluciones o cancelaciones)
            - Filas con 'Quantity' <= 0
            - Filas con 'UnitPrice' == 0

        Args:
            df (pd.DataFrame): DataFrame a filtrar.

        Returns:
            pd.DataFrame: DataFrame filtrado.
        """
        df = df[~df['InvoiceNo'].str.startswith('C', na=False)]
        df = df[df['Quantity'] > 0]
        df = df[df['UnitPrice'] != 0]
        return df

    def all_functions(self) -> pd.DataFrame:
        """
        Aplica todas las funciones de limpieza y transformación en orden:
        manejo de nulos, formateo
        de fecha, filtrado, y cálculo de precio total por ítem.

        Returns:
            pd.DataFrame: DataFrame transformado listo para la siguiente etapa.
        """
        df = self.dataframe.copy()
        df = self.handling_customer_na(df)
        df = self.handling_time(df)
        df = self.filtering(df)
        df['total_price_per_item'] = df['Quantity'] * df['UnitPrice']
        return df
