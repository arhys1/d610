import numpy as np
from sklearn.metrics import r2_score, mean_squared_error
from clean_data import run_cleaning_pipeline
from analyze_data import add_genre_dummies, prepare_regression_data, split_data, fit_ols_model

def evaluate_model_test(model, X_test, y_test, log_transformed=False):
    """
    Test version of evaluate_model — reports R-squared in log-space
    (no back-transformation) alongside the dollar-scale metrics.
    """
    import statsmodels.api as sm
    X_test_const = sm.add_constant(X_test)
    predictions = model.predict(X_test_const)

    if log_transformed:
        log_r2 = r2_score(y_test, predictions)
        print(f"Test R-squared (log scale): {log_r2:.4f}")

        predictions = np.exp(predictions)
        y_test = np.exp(y_test)

    r2 = r2_score(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions) ** 0.5

    print(f"Test R-squared: {r2:.4f}")
    print(f"Test RMSE: {rmse:.4f}")

    return r2, rmse

if __name__ == "__main__":
    df, df_application_genres, df_english_genres = run_cleaning_pipeline()
    df = add_genre_dummies(df, df_application_genres, df_english_genres)

    print('\n###MODEL 3 TEST: LOG-SPACE VS DOLLAR-SCALE R-SQUARED###')
    X_log, y_log = prepare_regression_data(
        df, drop_feature_cols=['metacritic_score', 'recommendations_total'],
        log_transform_target=True
    )
    X_train_log, X_test_log, y_train_log, y_test_log = split_data(X_log, y_log)
    model_log = fit_ols_model(X_train_log, y_train_log)
    evaluate_model_test(model_log, X_test_log, y_test_log, log_transformed=True)