"""Exposes common utilities."""

import os

import psycopg2
import pandas as pd
import sqlalchemy
import sklearn.metrics

import energy.selects as selects
import numpy as np

_CREATE_TABLE = """CREATE TABLE {table_name}
(
    {columns}
);
""".format

_DATA_TYPES_MAP = {
    'float32': 'REAL',
    'float64': 'REAL',
    'int64': 'INT',
    'datetime64[ns]': 'timestamp'
}


def make_engine():
    """Returns an engine."""
    return sqlalchemy.create_engine(selects.CONN_STR)

def save_to_db(data, table_name):
    """Creates a table to store the passed in data frame to the database.

    :param pd.DataFrame data: The data frame to save to the data base.
    :param str table_name: The name of the table to create.
    """
    data = data.dropna()
    conn = psycopg2.connect(selects.CONN_STR)
    cur = conn.cursor()
    cur.execute(f'drop table if exists {table_name}')

    columns = []
    for column_name, data_type in zip(list(data.columns), list(data.dtypes)):
        data_type = _DATA_TYPES_MAP[str(data_type)]
        columns.append(f'{column_name} {data_type}')

    sql_create_table = _CREATE_TABLE(
        table_name=table_name,
        columns=','.join(columns)
    )

    cur.execute(sql_create_table)
    conn.commit()

    filename = f'/vagrant/data/{table_name}.csv'
    with open(filename, 'w') as f:
        f.write(data.to_csv(index=False, header=False))

    sql = f"copy {table_name} FROM '{filename}' DELIMITER ',' CSV"
    cur.execute(sql)
    conn.commit()

    cur.execute(selects.SQL_INSERT_MEDIAN_DIFF_PER_HOUR)
    conn.commit()

    os.remove(filename)

import matplotlib.pyplot as plt
import seaborn as sns

def show_correlation_graph(data, title=None,
                           cmap=None, linewidths=0, figsize=(9, 6), annot=True):
    if cmap is None:
        cmap = sns.diverging_palette(10, 120, as_cmap=True)
    data = data.dropna()
    corr = data.corr()
    for column_name in corr.columns:
        corr[column_name] = corr[column_name].abs()
    _, ax = plt.subplots(figsize=figsize)
    if title:
        ax.set_title(title)

    _ = sns.heatmap(corr, annot=annot, fmt="2.2f",
                linewidths=linewidths, ax=ax, cmap=cmap)




def get_mean_squared_error(actual, predicted):
    return np.sqrt(sklearn.metrics.mean_squared_error(actual, predicted))


def feature_importance(the_model, features, scaler, labels, date_times):
    # Calculate feature importance
    feature_importances = []
    for column_name in features.columns:
        col = features[column_name].copy()
        try:
            features[column_name] = features[column_name].sample(frac=1).values
            reg_predictions = pd.DataFrame(scaler.inverse(the_model.predict(features)))
            reg_predictions[['expected']] = labels.load.values
            reg_predictions[['date_time']] = date_times.date_time.values
            reg_predictions.columns = ["predicted", 'expected', 'date_time']
            mse = get_mean_squared_error(reg_predictions.predicted.to_numpy(), reg_predictions.expected.to_numpy())
            feature_importances.append([column_name, mse])
        finally:
            features[column_name] = col
    feature_importances = pd.DataFrame(feature_importances, columns = ['Name', 'MSE Without it'])
    feature_importances = feature_importances.sort_values('MSE Without it',  ascending=False)
    show_correlation_graph(features, annot=False, title="Feature Correlations")
    print(feature_importances)
    feature_importances.plot.pie(
        y='MSE Without it', figsize=(7.5, 7.5),
        title="Feature Importance",
        labels=feature_importances["Name"],
        shadow=True
    )
    _ = plt.legend(loc='center left', bbox_to_anchor=(1.5, 0.5))


def pair_feature_importance(the_model, features, scaler, labels, date_times):
    # Calculate feature importance
    feature_importances = []
    for column_name in features.columns:
        col = features[column_name].copy()
        try:
            features[column_name] = features[column_name].sample(frac=1).values
            reg_predictions = pd.DataFrame(scaler.inverse(the_model.predict(features)))
            reg_predictions[['expected']] = labels.load.values
            reg_predictions[['date_time']] = date_times.date_time.values
            reg_predictions.columns = ["predicted", 'expected', 'date_time']
            mse = get_mean_squared_error(reg_predictions.predicted.to_numpy(), reg_predictions.expected.to_numpy())
            feature_importances.append([column_name, mse])
        finally:
            features[column_name] = col
    feature_importances = pd.DataFrame(feature_importances, columns = ['Name', 'MSE Without it'])
    feature_importances = feature_importances.sort_values('MSE Without it',  ascending=False)
    show_correlation_graph(features, annot=False, title="Feature Correlations")
    print(feature_importances)
    feature_importances.plot.pie(
        y='MSE Without it', figsize=(7.5, 7.5),
        title="Feature Importance",
        labels=feature_importances["Name"],
        shadow=True
    )
    _ = plt.legend(loc='center left', bbox_to_anchor=(1.5, 0.5))


if __name__ == '__main__':
    data = pd.DataFrame({'a': [1., 2, 3], 'b': [23, 34, 22]})
    save_to_db(data, 'junk')
