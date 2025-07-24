from complete_medallion.complete_medallion_all import (
    running_complete_medallion
)
from training.all_training import complete_training


def main() -> None:
    """
    Función principal para ejecutar el pipeline completo:
    - Ejecuta la ejecución completa del medallion (bronze, silver, gold).
    - Ejecuta el entrenamiento completo del modelo.
    """
    running_complete_medallion()
    complete_training()


if __name__ == "__main__":
    main()
