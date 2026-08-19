# ==============================================================================================
# The purpose of this .py file is to run the full pipeline end to end:
# importing, cleaning, and analyzing the dataset.
# ==============================================================================================

from clean_data import run_cleaning_pipeline
from analyze_data import (
    add_genre_dummies, prepare_regression_data, split_data, fit_ols_model, evaluate_model
)

def main():
    df, df_application_genres, df_english_genres = run_cleaning_pipeline()
    df = add_genre_dummies(df, df_application_genres, df_english_genres)

    print('\n###MODEL 1: WITH METACRITIC_SCORE AND RECOMMENDATIONS_TOTAL###')
    X_full, y_full = prepare_regression_data(df)
    X_train_full, X_test_full, y_train_full, y_test_full = split_data(X_full, y_full)
    model_full = fit_ols_model(X_train_full, y_train_full)
    print(model_full.summary())
    evaluate_model(model_full, X_test_full, y_test_full)

    print('\n###MODEL 2: WITHOUT METACRITIC_SCORE AND RECOMMENDATIONS_TOTAL###')
    X_reduced, y_reduced = prepare_regression_data(
        df, drop_feature_cols=['metacritic_score', 'recommendations_total']
    )
    X_train_reduced, X_test_reduced, y_train_reduced, y_test_reduced = split_data(X_reduced, y_reduced)
    model_reduced = fit_ols_model(X_train_reduced, y_train_reduced)
    print(model_reduced.summary())
    evaluate_model(model_reduced, X_test_reduced, y_test_reduced)

    print('\n###MODEL 3: LOG-TRANSFORMED TARGET (WITHOUT METACRITIC_SCORE/RECOMMENDATIONS_TOTAL)###')
    X_log, y_log = prepare_regression_data(
        df, drop_feature_cols=['metacritic_score', 'recommendations_total'], log_transform_target=True
    )
    X_train_log, X_test_log, y_train_log, y_test_log = split_data(X_log, y_log)
    model_log = fit_ols_model(X_train_log, y_train_log)
    print(model_log.summary())
    evaluate_model(model_log, X_test_log, y_test_log, log_transformed=True)

main()