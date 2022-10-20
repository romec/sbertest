CREATE_TABLE_SQL = """
create table if not exists deltas (
id integer primary key,
rep_dt date not null,
delta float not null
);
"""

TRUNCATE_TABLE_SQL = """
delete from deltas;
"""

SELECT_DELTA_SQL = """
select rep_dt, delta from deltas order by rep_dt;
"""

SELECT_DELTA_LAG_SQL = """
select rep_dt, delta, delta_lag from deltas_lag order by rep_dt;
"""

INSERT_DELTA_SQL = """
insert into deltas(rep_dt, delta) values (?, ?);
"""

CREATE_DELTA_LAG_VIEW_SQL = """
create temp view deltas_lag
as
select
    d1.rep_dt as rep_dt,
    d1.delta as delta,
    d2.rep_dt as rep_dt_lag,
    d2.delta as delta_lag
from deltas as d1
left join deltas as d2 on
    date(d1.rep_dt,'start of month') = date(d2.rep_dt,'start of month','+{0} month');
"""
