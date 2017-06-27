from utilities.getting_soup_from_web import BSoup

def bus_stop_minutes_remaining():
    '''IT LOOKS FOR THE BUS_STOP_NUMBER INPUT TO RETRIEVE MINUTES
       REMAINING FOR BUS_LINES TO ARRIVE TO THAT BUS_STOP'''
    #THREE OPTIONS: 1.BUS STOP DOESNT EXIST\2.EXISTS AND HAS INFO\
    #               3.EXISTS AND DOES NOT HAVE INFO
    busstop_number = 587  #Meter aqui el numero de parada que se quiera
    prompt = 'Insert Bus_stop Number please')
    bus_stopnumber = input(prompt)
    url = 'http://transportesrober.com:9055/websae/Transportes/parada.aspx?'+ \
          'idparada='+str(busstop_number)
    soup = BSoup(url)

    if(soup.head.get_text().strip() == 'error'):
        print('Bus stop does not exist') #aqui se podria meter pass...para eso esta

    else: 
        soup = soup.find_all('td','tabla_campo_valor')
        if soup:
            bus_line, busstop_name, minutes, counter = [] , [], [], 0

            for i,td in enumerate(soup):
                #We want data every three td in soup
                if (i%3 == 0):
                    bus_line.append(td.get_text().strip())
                elif (i%3 == 1):
                    busstop_name.append(td.get_text().strip())
                elif (i%3 == 2):
                    minutes.append(td.get_text().strip())
                counter +=1

            for i in range(0,int(counter/3)):
                print(minutes[i],' Minutes remaining for the bus_line to arrive ',
                      bus_line[i], ' a la parada', busstop_name[i],' numero: ',
                      busstop_number)
        else:
            print('There is no data for the input bus stop')


bus_stop_minutes_remaining()
