
from sklearn.model_selection import train_test_split


class TrainingClass:

    def __init__(self, dataframe):
        self.dataframe = dataframe

    def train_test_val(self, for_train_df):

        # Let's split data into train and test
        X_train, X_temp, y_train, y_temp = train_test_split(
            for_train_df.drop('Target_90Days', axis=1),
            for_train_df["Target_90Days"],
            test_size=0.3,
            random_state=1
        )

        # Then: validation (15%) and test (15%) from the 30% temp set
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp,
            y_temp,
            test_size=0.5,
            random_state=1
        )

        return X_train, X_val, X_test, y_val, y_test, y_train

    def quantile_inputation(self, X_train, X_test, X_val, column):
        lower_limit = X_train[column].quantile(0.05)
        upper_limit = X_train[column].quantile(0.95)
        X_train[column].clip(lower=lower_limit, upper=upper_limit,
                             inplace=True)
        X_test[column].clip(lower=lower_limit, upper=upper_limit, inplace=True)
        X_val[column].clip(lower=lower_limit, upper=upper_limit, inplace=True)

        return X_train, X_test, X_val

    def training_dataframes(self):

        for_train_df = self.dataframe.copy()

        (X_train,
         X_val,
         X_test,
         y_val,
         y_test,
         y_train) = self.train_test_val(for_train_df)
        columns = ['Quantity', 'total']
        for column in columns:
            (X_train,
             X_val,
             X_test
             ) = self.quantile_inputation(X_train, X_val, X_test, column)

        return X_train, X_val, X_test, y_val, y_test, y_train
