import pandas as pd
import numpy as np


class GoldClass:

    def __init__(self, dataframe):
        self.dataframe = dataframe

    def grouping(self, df):

        grouped_df = df.groupby(['CustomerID', 'DateColumn']).agg({
            'Quantity': 'sum',
            'total_price_per_item': 'sum',
            'Country': 'first'  # or 'mode', or a custom function
        }).reset_index()


        # We need to drop the null Customer because we can´t track the correct ID if it´s null
        grouped_df = grouped_df[grouped_df['CustomerID']!='0']
        grouped_df.rename({'total_price_per_item':'total'}, axis=1, inplace=True)
        grouped_df['DateColumn'] = pd.to_datetime(grouped_df['DateColumn'], format='%d-%m-%Y')
        grouped_df = grouped_df.sort_values(['CustomerID', 'DateColumn'])

        return grouped_df
    
    def creating_target(self, grouped_df):

        grouped_df['NextPurchaseDate'] = grouped_df.groupby('CustomerID')['DateColumn'].shift(-1)
        grouped_df['days_since_last_purchase'] = ((grouped_df['NextPurchaseDate'] - grouped_df['DateColumn']))
        grouped_df['days_since_last_purchase']=grouped_df['days_since_last_purchase'].dt.days
        grouped_df['days_since_last_purchase'] = grouped_df['days_since_last_purchase'].fillna(-1)
        grouped_df['days_since_last_purchase']=grouped_df['days_since_last_purchase'].astype('int')
        grouped_df['Target_90Days'] = np.where(
            (grouped_df['days_since_last_purchase']<=90
             ) & (grouped_df['days_since_last_purchase']!=-1), 1, 0)
        
        for_train_df = grouped_df[['Quantity', 'total', 'Target_90Days', 'Country']].copy()
        for_train_df['regroup_country'] = np.where(
            for_train_df['Country']=='United Kingdom', 'United Kingdom', 'other')
        
        for_train_df.drop('Country', axis=1, inplace=True)

        for_train_df['regroup_country'] = np.where(
            for_train_df['regroup_country']=='United Kingdom', 1, 0)

        return for_train_df
    
    def all_gold_functions(self):
        df = self.dataframe

        grouped_df = self.grouping(df)

        for_train_df = self.creating_target(grouped_df)

        return for_train_df
    


