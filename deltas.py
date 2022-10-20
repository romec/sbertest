from datetime import date
from math import isnan
from typing import List, Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

from constants import DEFAULT_MONTHS
from db import get_db
from sql import (
    INSERT_DELTA_SQL,
    TRUNCATE_TABLE_SQL,
    SELECT_DELTA_SQL,
    SELECT_DELTA_LAG_SQL,
    CREATE_TABLE_SQL,
    CREATE_DELTA_LAG_VIEW_SQL,
)
from domain import Row, RowLag
from utils import parse_rep_dt, parse_delta


def prepare_table():
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(CREATE_TABLE_SQL)
    cursor.execute(TRUNCATE_TABLE_SQL)


def insert(rows: List[Row]):
    connection = get_db()
    cursor = connection.cursor()
    cursor.executemany(INSERT_DELTA_SQL, [(r.rep_dt, r.delta) for r in rows])
    connection.commit()


def truncate():
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(TRUNCATE_TABLE_SQL)


def get_delta() -> List[Row]:
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(SELECT_DELTA_SQL)
    data = cursor.fetchall()
    return [Row(rep_dt=r[0], delta=r[1]) for r in data]


def create_delta_lag_view(months: Optional[int] = None):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(CREATE_DELTA_LAG_VIEW_SQL.format(months or DEFAULT_MONTHS))


def get_delta_lag() -> List[RowLag]:
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(SELECT_DELTA_LAG_SQL)
    data = cursor.fetchall()
    return [RowLag(rep_dt=r[0], delta=r[1], delta_lag=r[2]) for r in data]


def _fd(d: date):
    return date(d.year, d.month, day=1)


def get_delta_lag_pandas(df: pd.DataFrame, months: Optional[int] = None) -> List[RowLag]:
    df['Rep_dt'] = df['Rep_dt'].apply(parse_rep_dt)
    df['Delta'] = df['Delta'].apply(parse_delta)
    df['left_on'] = df.apply(
        lambda row: _fd(row['Rep_dt']),
        axis=1,
    )
    df['right_on'] = df.apply(
        lambda row: _fd(row['Rep_dt']) + relativedelta(months=months or DEFAULT_MONTHS),
        axis=1,
    )

    result = pd.merge(df, df, left_on='left_on', right_on='right_on', how='left')
    result.sort_values('Rep_dt_x', inplace=True)

    return [
        RowLag(
            rep_dt=r['Rep_dt_x'].isoformat(),
            delta=r['Delta_x'],
            delta_lag=None if isnan(r['Delta_y']) else r['Delta_y'],
        )
        for idx, r in result.iterrows()
    ]
