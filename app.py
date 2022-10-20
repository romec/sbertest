from flask import Flask, g, request

import controllers

app = Flask(__name__)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


###
# http://localhost:5000/import/xlsx
###
@app.route('/import/xlsx')
def import_xlsx():
    num_rows = controllers.import_xlsx()
    return {'result': num_rows, 'resultStr': 'OK'}


###
# http://localhost:5000/export/sql
# http://localhost:5000/export/sql?lag_num=1
# http://localhost:5000/export/sql?lag_num=10
# http://localhost:5000/export/sql?lag_num=100
###
@app.route('/export/sql')
def export_sql():
    months = request.args.get('lag_num')
    months = int(months) if months else None
    rows = controllers.export_sql(months)
    return {'result': rows, 'resultStr': 'OK'}


###
# http://localhost:5000/export/pandas
# http://localhost:5000/export/pandas?lag_num=1
# http://localhost:5000/export/pandas?lag_num=10
# http://localhost:5000/export/pandas?lag_num=100
###
@app.route('/export/pandas')
def export_pandas():
    months = request.args.get('lag_num')
    months = int(months) if months else None
    rows = controllers.export_pandas(months)
    return {'result': rows, 'resultStr': 'OK'}


if __name__ == '__main__':
    app.run()
