import sqlite3

import pandas as pd

from utilities.idlinea import retrieve_bus_line

def conexion_db(bus_line_id):
    '''RETRIEVES INFO ABOUT LINE ANALYSIS FOR THE ID_LINE INPUT BY THE
       USER'''
###LO QUE ESTA ENTRE LAS ALMOHADILLAS HAY QUE CAMBIARLO PARA QUE ACCEDA A
## LA DB CORRECTA Y QUE NOS DE EL NOMBRE DE TODOS LOS TRAYECTOS...
    db_name = '..\..\Data\Web_crawling_T.Rober'
    db_name += '\horabuses.db'
    conn_horasu3 = sqlite3.connect(db_name)
    realtimebusDF = pd.read_sql('SELECT * FROM iIdLinea_{0}'.format(bus_line_id),
                              con = conn_horasu3,parse_dates = ['index'])

########################################
    conn_horasu3.close()

    realtimebusDF = realtimebusDF.set_index(['index'],drop=True)
    realtimebusDF = realtimebusDF.apply(lambda x: pd.to_numeric(x))

    print(realtimebusDF)
    print(realtimebusDF.info())

bus_line_id = retrieve_bus_line()
conexion_db(bus_line_id)



