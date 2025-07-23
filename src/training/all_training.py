
from training.training_functions import TrainingClass
from training.model_training import trainer
from training.bring_gold import gold_dataframe


def complete_training():
    gold_data = gold_dataframe()

    train = TrainingClass(gold_data)
    X_train, X_val, X_test, y_val, y_test, y_train = train.training_dataframes()
    model = trainer(X_train, X_val, X_test, y_val, y_test, y_train)

    return model
    







