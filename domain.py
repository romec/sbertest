from dataclasses import dataclass
from datetime import date


@dataclass
class Row:
    rep_dt: date
    delta: float


@dataclass
class RowLag:
    rep_dt: date
    delta: float
    delta_lag: float
