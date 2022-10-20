from typing import Any, List

import pandas as pd
from pyexcel_xlsx import get_data

from constants import XLSX_FILENAME, SHEET_NAME
from domain import Row
from utils import parse_rep_dt, parse_delta


def read_xlsx():
    data = get_data(XLSX_FILENAME, sheet_name=SHEET_NAME)
    return data[SHEET_NAME]


def clean_table(table: List[Any]) -> List[Row]:
    result = []
    for rep_dt_raw, delta_raw in table[1:]:  # table[1:] = skip header row
        result.append(Row(rep_dt=parse_rep_dt(rep_dt_raw), delta=parse_delta(delta_raw)))
    return result


def get_dataframe() -> pd.DataFrame:
    xl_file = pd.ExcelFile(XLSX_FILENAME)
    dfs = {sheet_name: xl_file.parse(sheet_name) for sheet_name in xl_file.sheet_names}
    return dfs[SHEET_NAME]
