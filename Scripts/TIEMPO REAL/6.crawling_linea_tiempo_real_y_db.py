import requests
import datetime
import time

import pandas as pd
import sqlite3

from utilities.idlinea import retrieve_bus_line

bus_line_id = retrieve_bus_line()
url = 'http://transportesrober.com:9055/WEBSAE/ajax/linea,Net.Web.Granada'
url += '.ashx?_method=BuscarAutobusesEnMarcha&_session=no'
data = {'iIdLinea':'{0}'.format(bus_line_id)}

while(True):
    day = str(datetime.datetime.now().year)+'_'
    day += str(datetime.datetime.now().month)+'_'
    day += str(datetime.datetime.now().day)
    db_name = '..\..\Data\Web_crawling_T.Rober'
    db_name += '\horabus{0}_{1}.db'.format(bus_line_id,day)
    
    conn_bustimes = sqlite3.connect(db_name)
    bustimesDF = pd.DataFrame(
        columns=['iidautobus','iminutosparallegar','iidlinea','iidparada',
                 'iidtrayecto','iordenEnTrayecto'])
    r = requests.post(url,data = data)
    r = r.text.split('[')[1].lstrip('{').rstrip('}]}').split('},{')
    time_hour = datetime.datetime.now()
    for bus in r:
        columnas = bus.split(',')
        
        for element,column_ in enumerate(columns_):
            columns_[element] = column_.split(':')[1]
        bustimesDF = bustimesDF.append(pd.DataFrame(
            {'iidautobus':columns_[0],
             'iminutosparallegar':columns_[1],
             'iidlinea':columns_[2],
             'iidparada':columns_[3],
             'iidtrayecto':columns_[4],
             'iordenEnTrayecto':columns_[5]},
            index=[time_hour]))
    print(bustimesDF)
    bustimesDF.to_sql('iIdLinea_525',con= conn_bustimes,if_exists = 'append')
    conn_bustimes.close()
    time.sleep(30)
