from training.training_functions import TrainingClass
from training.model_training import trainer
from training.bring_gold import gold_dataframe
from training.outputs_table import outputs
from typing import Any  # Ajusta según el tipo real de 'model'


def complete_training() -> Any:
    """
    Ejecuta el pipeline completo de entrenamiento:
    - Carga los datos Gold desde la base de datos.
    - Prepara los datasets de entrenamiento, validación y prueba.
    - Entrena el modelo usando los datasets preparados.
    - Guarda o procesa las salidas necesarias.

    Returns:
        model: El modelo entrenado resultante.
    """
    gold_data = gold_dataframe()

    train = TrainingClass(gold_data)
    (X_train, X_val,
     X_test,
     y_val,
     y_test,
     y_train,
     dict_quantiles) = train.training_dataframes()
    model = trainer(X_train, X_val, X_test, y_val, y_test, y_train)
    outputs()

    return model
