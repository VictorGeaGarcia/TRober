import sqlite3
import pandas as pd
from utilities.idlinea import retrieve_linea

def conexion_db(id_linea):

###LO QUE ESTA ENTRE LAS ALMOHADILLAS HAY QUE CAMBIARLO PARA QUE ACCEDA A
## LA DB CORRECTA Y QUE NOS DE EL NOMBRE DE TODOS LOS TRAYECTOS...
    db_name = '..\..\Data\Web_crawling_T.Rober'
    db_name += '\horabuses.db'
    conn_horasu3 = sqlite3.connect(db_name)
    horabusu3DF = pd.read_sql('SELECT * FROM iIdLinea_{0}'.format(id_linea),
                              con = conn_horasu3,parse_dates = ['index'])

########################################
    conn_horasu3.close()

    horabusu3DF = horabusu3DF.set_index(['index'],drop=True)
    horabusu3DF = horabusu3DF.apply(lambda x: pd.to_numeric(x))

    print(horabusu3DF)
    print(horabusu3DF.info())

#Se le pide al usuario que indique la linea de la quiere obtener la info sobre
#el analisis de sus horarios
    
id_linea = retrieve_linea()
conexion_db(id_linea)



