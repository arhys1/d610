# ==============================================================================================
# The purpose of this .py file is to analyze the cleaned Steam data using multiple regression
# ==============================================================================================

import pandas as pd
from clean_data import run_cleaning_pipeline
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np

### build genre_multihot encoding

def build_genre_multihot(df_application_genres, df_english_genres):
    """
    Builds a one-row-per-appid table with one binary column per English genre,
    True if the app belongs to that genre. Allows a game to belong to
    multiple genres without duplicating rows.
    """
    merged = df_application_genres.merge(
        df_english_genres.rename(columns={'id': 'english_genre_id', 'name': 'genre_name'}),
        on='english_genre_id',
        how='left'
    )

    genre_multihot = pd.crosstab(merged['appid'], merged['genre_name']) > 0
    genre_multihot = genre_multihot.add_prefix('genre_').reset_index()

    return genre_multihot

def add_genre_dummies(df, df_application_genres, df_english_genres):
    """
    Merges the multi-hot genre table onto df, keeping one row per game.
    """
    genre_multihot = build_genre_multihot(df_application_genres, df_english_genres)

    df = df.merge(genre_multihot, on='appid', how='left')

    genre_cols = [c for c in df.columns if c.startswith('genre_')]
    df[genre_cols] = df[genre_cols].infer_objects(copy=False)

    return df

### build regression pipeline
def prepare_regression_data(df, target_col='mat_final_price', drop_feature_cols=None):
    """
    Builds X (features) and y (target) for regression.
    Drops identifier/non-feature columns and the other price-related
    columns (to avoid leaking the target through mat_initial_price /
    mat_discount_percent).
    Drops rows with nulls in any remaining feature columns, since OLS
    cannot fit on missing values.
    Creates a drop_feature_cols list to remove columns with many nulls for a more robust analysis on other variables.
    If log_transform_target is True, applies np.log() to the target column,
    since price is right-skewed. Coefficients on a log-transformed target
    represent approximate percentage effects rather than dollar effects.
    """
    drop_cols = ['appid', 'name', 'release_date', 'mat_initial_price', 'mat_discount_percent']
    if drop_feature_cols:
        drop_cols += drop_feature_cols

    model_df = df.drop(columns=drop_cols)

    before_count = len(model_df)
    model_df = model_df.dropna()
    after_count = len(model_df)
    print(f"Dropped {before_count - after_count} rows with missing values in remaining feature columns "
          f"({before_count} -> {after_count})")

    genre_cols = [c for c in model_df.columns if c.startswith('genre_')]
    model_df[genre_cols] = model_df[genre_cols].astype(int)

    y = model_df[target_col]
    if log_transform_target:
        y = np.log(y)
    X = model_df.drop(columns=[target_col])

    return X, y

def split_data(X, y, test_size=0.2, random_state=42):
    """
    Splits X and y into train/test sets. random_state fixes the split
    so results are reproducible across runs.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    return X_train, X_test, y_train, y_test

def fit_ols_model(X_train, y_train):
    """
    Fits an OLS regression model using statsmodels, which provides
    coefficients, p-values, R-squared, and a full summary table.
    """
    X_train_const = sm.add_constant(X_train)
    model = sm.OLS(y_train, X_train_const).fit()
    return model

def evaluate_model(model, X_test, y_test, log_transformed=False):
    """
    Evaluates the fitted model on held-out test data using R-squared
    and RMSE. If log_transformed is True, exponentiates both predictions
    and actuals back to dollar scale before computing RMSE, so the error
    is reported in real dollars rather than log-dollars.
    """
    X_test_const = sm.add_constant(X_test)
    predictions = model.predict(X_test_const)

    if log_transformed:
        predictions = np.exp(predictions)
        y_test = np.exp(y_test)

    r2 = r2_score(y_test, predictions)
    rmse = mean_squared_error(y_test, predictions) ** 0.5

    print(f"Test R-squared: {r2:.4f}")
    print(f"Test RMSE: {rmse:.4f}")

    return r2, rmse

## test full pipeline: genre dummies, then both regression models
if __name__ == "__main__":
    df, df_application_genres, df_english_genres = run_cleaning_pipeline()

    print('\n###TEST ADD_GENRE_DUMMIES###')
    before_rows = len(df)
    df = add_genre_dummies(df, df_application_genres, df_english_genres)
    after_rows = len(df)

    print(f'\nROW COUNT BEFORE: {before_rows}, AFTER: {after_rows} (these should match — one row per game)')

    print('\nCOLUMNS AFTER ADDING DUMMIES')
    print(df.columns.tolist())

    print('\nHEAD OF df')
    print(df.head())

    print('\nSAMPLE ROW WHERE A GAME HAS MULTIPLE GENRES TRUE')
    genre_cols = [c for c in df.columns if c.startswith('genre_')]
    multi_genre_sample = df[df[genre_cols].sum(axis=1) > 1]
    print(multi_genre_sample[['appid', 'name'] + genre_cols].head().to_string())

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