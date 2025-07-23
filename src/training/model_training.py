

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier
import xgboost
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score
import mlflow
import mlflow.sklearn
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_score
import joblib

def trainer(X_train, X_val, X_test, y_val, y_test, y_train):
    counts = y_train.value_counts()
    coeff = counts[1] / counts[0]

    models = [
        RandomForestClassifier(),
        GradientBoostingClassifier(),
        xgboost.XGBClassifier(scale_pos_weight=coeff)
    ]
    models_names = ['random', 'gradient', 'xgb']
    models_scores = {}
    models_trained = {}

    for name, model in zip(models_names, models):
        with mlflow.start_run(run_name=name):
            pipeline_model = Pipeline([
                ('standard', StandardScaler()),
                (name, model)
            ])
            pipeline_model.fit(X_train, y_train)
            y_pred = pipeline_model.predict(X_val)
            precision = precision_score(y_val, y_pred, zero_division=0)

            # Log parameters
            mlflow.log_param("model_name", name)
            if name == 'xgb':
                mlflow.log_param("scale_pos_weight", coeff)

            # Log metric
            mlflow.log_metric("val_precision", precision)

            # Log model
            mlflow.sklearn.log_model(pipeline_model, artifact_path="model")

            # Store for final evaluation
            models_scores[name] = precision
            models_trained[name] = pipeline_model

    # Evaluate best model on test
    max_precision_model = max(models_scores, key=models_scores.get)
    final_model = models_trained[max_precision_model]
    final_pred = final_model.predict(X_test)
    final_precision = precision_score(y_test, final_pred, zero_division=0)

    # Log best model test precision
    with mlflow.start_run(run_name="best_model_test", nested=True):
        mlflow.log_param("best_model", max_precision_model)
        mlflow.log_metric("test_precision", final_precision)
        mlflow.sklearn.log_model(final_model, artifact_path="best_model")
    
    # Optional: also save locally
    joblib.dump(final_model, 'model.pkl')

    return final_model



    # return max_precision_model, models_trained[max_precision_model], final_precision