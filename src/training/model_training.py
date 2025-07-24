

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import precision_score
from xgboost import XGBClassifier
import joblib


def trainer(X_train, X_val, X_test, y_val, y_test, y_train):

    counts = y_train.value_counts()

    # Calculate coefficient: count of 1s divided by count of 0s
    coeff = counts[1] / counts[0]

    models = [RandomForestClassifier(),
              GradientBoostingClassifier(),
              XGBClassifier(scale_pos_weight=coeff)]

    models_names = ['random', 'gradient', 'xgb']

    models_scores = {}
    models_trained = {}

    for name, model in zip(models_names, models):
        pipeline_model = Pipeline([(
            'standard', StandardScaler()), (name, model)])

        pipeline_model.fit(X_train, y_train)

        y_pred = pipeline_model.predict(X_val)

        precision = precision_score(y_val, y_pred, zero_division=0)

        models_scores[name] = precision
        models_trained[name] = pipeline_model

    max_precision_model = max(models_scores, key=models_scores.get)
    final_pred = models_trained[max_precision_model].predict(X_test)
    final_precision = precision_score(y_test, final_pred, zero_division=0)
    print(final_precision)

    joblib.dump(models_trained[max_precision_model], 'model.pkl')

    return models_trained[max_precision_model]

    # return max_precision_model,
    # models_trained[max_precision_model], final_precision
