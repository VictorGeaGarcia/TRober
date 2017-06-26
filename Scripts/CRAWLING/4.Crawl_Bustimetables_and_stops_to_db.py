from utilities.getting_soup_from_web import BSoup
import pandas as pd
import sqlite3

def user_options():
    '''USER INTERFACE SO THAT IT CAN BE CHOSEN WHAT HE/SHE WANTS TO DO'''
    prompt = '\nChoose one of the following options:'
    prompt += '\n --> "1" OBTAIN A DATABASE WITH TIMETABLE FOR EVERY LINE'
    prompt += '\n --> "2" OBTAIN A DATABASE WITH BUS_STOPS FOR EVERY LINE'
    prompt += '\n --> "3" OBTAIN A DATABASE WITH BOTH TIMETABLES AND '+ \
              'BUS_STOPS FOR EVERY LINE\n "q" to quit\n'
    active = True
    while active:
        user_choice = input(prompt)
        if user_choice == '1':
            timetables(id_web, num_linea)
        elif user_choice == '2':
            bus_stops(id_web, num_linea)
        elif user_choice == '3':
            timetables(id_web, num_linea)
            bus_stops(id_web, num_linea)
        elif user_choice == 'q':
            break
        else:
            print('You must choose either one of the three options, or quit'+ \
                  '\nType: "1" "2" "3", or "q"')
            active = True
            
def soup_timetables(id_, name):
    '''RETRIEVES THE SOUP AFTER SCRAPING THE TIMETABLE WEBPAGE'''
    url_timetables =  'http://transportesrober.com:9055/websae/Transportes'
    url_timetables += '/horario.aspx?id={0}&tipo=L&nombre={1}&fecha=17/02/'
    url_timetables += '2017&desde_horario=si'
    url_timetables = url_timetables.format(id_, name)
    return BSoup(url_timetables).find('div', {'id':'PanelHorario'}) 

def obtain_routes(id_, name):
    '''RETRIEVES THE ROUTES FOR A CERTAIN LINE'''
    soup = soup_timetables(id_, name)
##    print(soup)
    if (bool(soup)):     
        routes = soup.find_all('td', {'class':'tablacabecera'})
        return(routes)
    else:
        lines_not_found.append(name)
        print('Line not found:', lines_not_found)

def timetables(id_web, line_web_names): 
    '''RETRIEVES ALL BUS_TIMETABLE FOR EACH BUS_LINE
       AND POPULATE A DB WITH ITS VALUES'''
    conn_timetables   = sqlite3.connect('timetables_Trober.db')

    for id_, name in zip(id_web, line_web_names):
        routes = []
        routes = obtain_routes(id_, name)
        soup = soup_timetables(id_, name)

        if (routes):
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
                conn_timetables.commit()
            
    conn_timetables.close()
            
def bus_stops(id_web, line_web_names):
    '''RETRIEVES ALL BUS_STOPS FOR EACH BUS_LINE
       AND POPULATE A DB WITH ITS VALUES'''
    conn_bus_stops = sqlite3.connect('bus_stops_Trober.db')

    for id_, name in zip(id_web, line_web_names):
        url_bus_stops = 'http://transportesrober.com:9055/websae/Transportes/'
        url_bus_stops += 'linea.aspx?idlinea='+str(id_)
        soup = BSoup(url_bus_stops)
        routes = []
        routes = obtain_routes(id_, name)
        if (bool(soup) and bool(routes)):
            for i, route in enumerate(routes):
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
                busstopsDF.to_sql(table_name, conn_bus_stops, index=False)
                conn_bus_stops.commit()
        else: 
            lines_not_found.append(name)

    conn_bus_stops.close()

web_codesDF = pd.read_csv('lista_lineas_horarios.csv',
                               index_col = 'Unnamed: 0')
web_codesDF      = web_codesDF.reset_index(drop=True)
id_web           = web_codesDF.id_web.values
num_linea        = web_codesDF.num_linea.values

lines_not_found = [] 
user_options()
