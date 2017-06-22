import requests
import pandas as pd
import datetime
import time
import sqlite3
from utilities.idlinea import retrieve_linea

id_linea = retrieve_linea()
url = 'http://transportesrober.com:9055/WEBSAE/ajax/linea,Net.Web.Granada'+ \
      '.ashx?_method=BuscarAutobusesEnMarcha&_session=no'
data = {'iIdLinea':'{0}'.format(id_linea)}

while(True):
    dia = str(datetime.datetime.now().year)+'_'+str(datetime.datetime.now().month)+'_'+str(datetime.datetime.now().day)
    conn_horabuses = sqlite3.connect('horabus{0}_{1}.db'.format(id_linea,dia))
    horabusesDF = pd.DataFrame(
        columns=['iidautobus','iminutosparallegar','iidlinea','iidparada',
                 'iidtrayecto','iordenEnTrayecto'])
    r = requests.post(url,data = data)
    r = r.text.split('[')[1].lstrip('{').rstrip('}]}').split('},{')
    hora = datetime.datetime.now()
    for autobus in r:
        columnas = autobus.split(',')
        
        for elemento,columna in enumerate(columnas):
            columnas[elemento] = columna.split(':')[1]
        horabusesDF = horabusesDF.append(pd.DataFrame(
            {'iidautobus':columnas[0],
             'iminutosparallegar':columnas[1],
             'iidlinea':columnas[2],
             'iidparada':columnas[3],
             'iidtrayecto':columnas[4],
             'iordenEnTrayecto':columnas[5]},
            index=[hora]))
    print(horabusesDF)
    horabusesDF.to_sql('iIdLinea_525',con= conn_horabuses,if_exists = 'append')
    conn_horabuses.close()
    time.sleep(30)
