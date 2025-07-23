import pandas as pd

class SilverClass:

    def __init__(self, dataframe):
        self.dataframe = dataframe

    def handling_customer_na(self, df):
        df['CustomerID'] = df['CustomerID'].fillna(0)
        df['CustomerID'] = df['CustomerID'].astype('int').astype('str')
        return df
    
    def handling_time(self, df):
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], format='%m/%d/%Y %H:%M')

        # Format to 'd-m-y' as string
        df['DateColumn'] = df['InvoiceDate'].dt.strftime('%d-%m-%Y')
        return df
    
    def filtering(self, df):
        df = df[~df['InvoiceNo'].str.startswith('C', na=False)]
        df = df[df['Quantity']>0]
        df = df[df['UnitPrice'] !=0]

        return df

    def all_functions(self):
        df = self.dataframe
        df = self.dataframe.copy()
        df = self.handling_customer_na(df)
        df = self.handling_time(df)
        df = self.filtering(df)
        df['total_price_per_item'] = df['Quantity']*df['UnitPrice']

        return df





        