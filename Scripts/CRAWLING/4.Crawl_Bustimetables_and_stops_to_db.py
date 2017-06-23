from utilities.getting_soup_from_web import BSoup
import pandas as pd
import sqlite3

def timetables(id_web, line_web_names):
    '''RETRIEVES ALL BUS_TIMETABLE FOR EACH BUS_LINE AND POPULATE A DB WITH ITS VALUES'''
    conn_timetables   = sqlite3.connect('timetables_Trober.db')

    lines_not_found   = [] #por si no entra,sabemos en que linea no ha entrado
    for id_, name in zip(id_web, line_web_names):
        routes = []
        url_timetables =  'http://transportesrober.com:9055/websae/Transportes/hora'
        url_timetables += 'rio.aspx?id={0}&tipo=L&nombre={1}&fecha=17/02/2017&desde'
        url_timetables += '_horario=si'
        url_timetables = url_timetables.format(id_, name)
        print(url_timetables)
        soup = BSoup(url_timetables).find('div', {'id':'PanelHorario'})
        print('Id: ', id_, '\nNombre: ', name)
        if (bool(soup)):     
            routes = soup.find_all('td', {'class':'tablacabecera'})
            for i, route in enumerate(routes):
                timetableDF   = pd.DataFrame(
                    columns = ['bus_line', 'route', 'timetable'])
                table_name = '{}'.format(name)+'_'+ \
                               '_'.join(route.text.strip().split())
                table_name = table_name.replace('-', '').replace('__', '_')
                table_name = table_name.replace(' ', '')
                table_timetable = soup.find_all('table')[2+i]

                rows = table_timetable.find_all('tr')
                tr_times = []
                for row in rows:
                    tr_times.extend(row.text.split(':', 1)[1].split(','))

                timetableDF = timetableDF.append(
                    pd.DataFrame(
                        {'bus_line':name, 'route':table_name,
                         'timetable':tr_times},
                        columns=['bus_line', 'route', 'timetable']))
                
                timetableDF.to_sql(table_name, conn_timetables, index=False)
                conn_horas.commit()
        else: 
            lines_not_found.append(name)

    conn_timetables.close()
            
def bus_stops(id_web, line_web_names):
    '''RETRIEVES ALL BUS_STOPS FOR EACH BUS_LINE AND POPULATE A DB WITH ITS VALUES'''
    conn_bus_stops = sqlite3.connect('bus_stops_Trober.db')

    lines_not_found = [] #por si no entra,sabemos linea no ha entrado

    for id_, name in zip(id_web, line_web_names):
        url_bus_stops = 'http://transportesrober.com:9055/websae/Transportes/'+ \
                      'linea.aspx?idlinea='+str(id_)
        soup = BSoup(url_bus_stops)
        if (bool(soup) & bool(routes)):
           for i, route in enumerate(routes):????? AQUI HAY UN PROBLEMA, AL HABER PARTIDO EN DOS FUNCIONES, NO TENEMOS LAS RUTAS AHORA. MODULAR ESA PARTE DE LA FUNCION ANTERIOR
                busstopsDF = pd.DataFrame(columns = ['busstop', 'transfer'])
            
                table_name = '{}'.format(name)+'_'+\
                               '_'.join(route.text.strip().split())
                table_name = table_name.replace(
                    '-','').replace('__','_').replace(' ', '')                
                route = soup.find_all('tr', {'class':'tabla_campo_valor'})

                for bus_stop in route:
                    bus_stops = bus_stop.find_all('tr')
                    bus_stop = bus_stops[0].find('a', {'class':'texto'}).text
                    transfers = []

                    for transfer in bus_stops[2].find_all(
                        'a', {'class':'texto'}):                        
                        transfers.append(transfer.text)
                    
                    transfers = ' '.join(transfers)

                    busstopsDF = busstopsDF.append(
                        pd.DataFrame(data = [[bus_stop, transfers]],
                                     columns=['busstop', 'transfer']))
                busstopsDF.to_sql(table_name, conn_busstops, index=False)
                conn_paradas.commit()
        else: 
            lines_not_found.append(nombre)

    conn_busstops.close()

web_codesDF = pd.read_csv('lista_lineas_horarios.csv',
                               index_col = 'Unnamed: 0')
web_codesDF = web_codesDF.reset_index(drop=True)
id_web           = web_codesDF.id_web.values
num_linea        = web_codesDF.num_linea.values
timetables(id_web, num_linea)
bus_stops(id_web, num_linea)
