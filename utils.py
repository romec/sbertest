from datetime import date
from typing import Union

from dateutil.parser import parse


def parse_rep_dt(rep_dt_raw) -> date:
    return parse(rep_dt_raw).date()


def parse_delta(delta_raw: Union[str, int, float]) -> float:
    if isinstance(delta_raw, float):
        return delta_raw
    if isinstance(delta_raw, str):
        return float(delta_raw.replace(',', '.'))
    if isinstance(delta_raw, int):
        return float(delta_raw)
    raise Exception('delta: unknown type')
