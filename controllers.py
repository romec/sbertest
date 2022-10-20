from typing import List, Optional

from deltas import (
    prepare_table,
    insert,
    create_delta_lag_view,
    get_delta_lag,
    get_delta,
    get_delta_lag_pandas,
)
from domain import Row, RowLag
from xlsx import read_xlsx, clean_table, get_dataframe


def import_xlsx() -> List[Row]:
    """
    Если таблица в базе есть, она очищается, иначе – создается
    Импортируемые данные приводятся к формату SQL-таблицы и загружаются в базу
    """
    prepare_table()
    raw_data = read_xlsx()
    cleaned_data = clean_table(raw_data)
    insert(cleaned_data)
    return get_delta()


def export_sql(months: Optional[int] = None) -> List[RowLag]:
    """
    Требуется создать Представление(VIEW) к SQL-таблице deltas
    В Представлении нужно сформировать новое поле DeltaLag путем смещения данных в поле Delta на 2 месяца назад
    """
    create_delta_lag_view(months)
    rows = get_delta_lag()
    return rows


def export_pandas(months: Optional[int] = None) -> List[RowLag]:
    """
    Смещение требуется реализовать на стороне Python средствами библиотеки Pandas
    """
    df = get_dataframe()
    rows = get_delta_lag_pandas(df, months)
    return rows
