import sqlite3
import pandas as pd
from utilities.idlinea import retrieve_linea

def conexion_db(id_linea):
    conn_horasu3 = sqlite3.connect('E:\Backup\DataAnalytics-Computing\Python'+ \
                                   '\Proyecto SETIC\Sistema Integral\Crawling'+ \
                                   '\DBs&CSVs\Web_crawling_T.Rober\horabuses.db')
    horabusu3DF = pd.read_sql('SELECT * FROM iIdLinea_{0}'.format(id_linea),
                              con = conn_horasu3,parse_dates = ['index'])
    conn_horasu3.close()

    horabusu3DF = horabusu3DF.set_index(['index'],drop=True)
    horabusu3DF = horabusu3DF.apply(lambda x: pd.to_numeric(x))

    print(horabusu3DF)
    print(horabusu3DF.info())

#Se le pide al usuario que indique la linea de la quiere obtener la info sobre
#el analisis de sus horarios
    
id_linea = retrieve_linea()
conexion_db(id_linea)



