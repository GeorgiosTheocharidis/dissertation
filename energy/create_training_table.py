"""Creates the table to be used for training and testing a model."""

import random

import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from scipy import stats

import energy.selects as selects
import energy.utils as utils

random = random.random

SQL_LOADER = """select
        extract(hour from a.date_time) as hour,
        a.date_time,
        a.next_hour_load_diff as data_diff,
        (avg(a.next_hour_load_diff)  over (rows between 1 preceding and current row)) as diff1,
        (avg(a.next_hour_load_diff)  over (rows between 2 preceding and current row)) as diff2,
        (avg(a.next_hour_load_diff)  over (rows between 3 preceding and current row)) as diff3,
        (avg(a.next_hour_load_diff)  over (rows between 5 preceding and current row)) as diff5,
        (avg(a.next_hour_load_diff)  over (rows between 8 preceding and current row)) as diff8,
        (avg(a.next_hour_load_diff)  over (rows between 13 preceding and current row)) as diff13,
        (avg(a.next_hour_load_diff)  over (rows between 24 preceding and current row)) as diff24,
        (avg(a.next_hour_load_diff)  over (rows between 37 preceding and current row)) as diff37,
        (avg(a.load)  over (rows between 1 preceding and current row)) as load1,
        (avg(a.load)  over (rows between 2 preceding and current row)) as load2,
        (avg(a.load)  over (rows between 3 preceding and current row)) as load3,
        (avg(a.load)  over (rows between 5 preceding and current row)) as load5,
        (avg(a.load)  over (rows between 8 preceding and current row)) as load8,
        (avg(a.load)  over (rows between 13 preceding and current row)) as load13,
        (avg(a.load)  over (rows between 24 preceding and current row)) as load24,
        (avg(a.load)  over (rows between 37 preceding and current row)) as load37,
        lag(a.load, 1) over (order by a.date_time) as laged_load_1,   
        lag(a.load, 2) over (order by a.date_time) as laged_load_2,    
        lag(a.load, 3) over (order by a.date_time) as laged_load_3,    
        lag(a.load, 5) over (order by a.date_time) as laged_load_5,
        lag(a.load, 8) over (order by a.date_time) as laged_load_8,
        lag(a.load, 13) over (order by a.date_time) as laged_load_13,
        lag(a.load, 24) over (order by a.date_time) as laged_load_24,
        lag(a.load, 37) over (order by a.date_time) as laged_load_37,
        b.price_actual,
        b.price_day_ahead,
        a.load as load
    From
        master a, energy b
    where
        a.date_time = b.date_time 
    """

SQL_LOAD_DIFFS = """
select 
    extract(hour from date_time) as hour, 
    next_hour_load_diff 
from 
    master 
"""

def create_training_table(table_name):
    np.set_printoptions(precision=3, suppress=True)
    engine = create_engine(selects.CONN_STR)

    all_data = pd.read_sql_query(SQL_LOADER, con=engine)
    all_data.describe().transpose()

    sql = SQL_LOAD_DIFFS
    data = pd.read_sql_query(sql, con=engine)

    data1 = data[(np.abs(stats.zscore(data.next_hour_load_diff)) < 3)]

    median_values = data1.groupby(data1.hour)[['next_hour_load_diff']].median()
    median_values = median_values.to_dict()['next_hour_load_diff']

    std_values = data1.groupby(data1.hour)[['next_hour_load_diff']].std()
    std_values = std_values.to_dict()['next_hour_load_diff']

    all_data['median_diff'] = all_data.apply(
        lambda row: median_values[row.hour], axis=1
    )

    all_data['median_std'] = all_data.apply(
        lambda row: std_values[row.hour],
        axis=1
    )

    mean = float(all_data.data_diff.mean())
    std = float(all_data.data_diff.std().mean())

    high_move = mean + 1 * std
    low_move = mean - 1 * std

    very_high_move = mean + 2 * std
    very_low_move = mean - 2 * std

    all_data['median_diff'] = all_data.apply(
        lambda row: median_values[row.hour],
        axis=1
    )

    all_data['median_std'] = all_data.apply(
        lambda row: std_values[row.hour],
        axis=1
    )

    all_data['very_high_move'] = all_data.apply(
        lambda row: 1 if row["data_diff"] >= very_high_move else 0,
        axis=1
    )

    all_data['very_low_move'] = all_data.apply(
        lambda row: 1 if row["data_diff"] <= very_low_move else 0,
        axis=1
    )

    all_data['high_move'] = all_data.apply(
        lambda row: 1 if very_high_move >= row["data_diff"] >= high_move else 0,
        axis=1
    )

    all_data['low_move'] = all_data.apply(
        lambda row: 1 if very_low_move <= row["data_diff"] <= low_move else 0,
        axis=1
    )

    all_data['no_move'] = all_data.apply(
        lambda row: 1 if low_move <= row["data_diff"] <= high_move else 0,
        axis=1
    )

    all_data['z_score'] = all_data.apply(
        lambda row: (row["data_diff"] - median_values[row.hour]) / std_values[row.hour],
        axis=1
    )


    # Shuffle the data rows.
    all_data = all_data.sample(frac=1.0)

    all_data['train'] = all_data.apply(lambda row: 1 if random() <= 0.8 else 0,
                                       axis=1)

    utils.save_to_db(all_data, table_name)


if __name__ == '__main__':
    create_training_table('junk')