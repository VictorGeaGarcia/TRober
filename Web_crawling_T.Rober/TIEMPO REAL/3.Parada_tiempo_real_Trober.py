from utilities.getting_soup_from_web import BSoup

#Aqui ya todo completo. Hay 3 opciones posibles
        #1. La parada no existe, entonces esto entrara en el primer if
        #2. La parada existe y tiene informacion, de una o varias lineas, eso es
        #   independiente,se imprime la info
        #3. La parada existe pero no hay info, puede ser que se trate de una
        #   parada que ya no funciona, que solo funciona por ejemplo en feria,
        #   o bien que no este en funcionamiento la linea en la hora seleccionada

num_parada = 587  #Meter aqui el numero de parada que se quiera

url = 'http://transportesrober.com:9055/websae/Transportes/parada.aspx?'+ \
      'idparada='+str(num_parada)
soup = BSoup(url)

if(soup.head.get_text().strip() == 'error'):
    print('La parada no existe') #aqui se podria meter pass...para eso esta

else: 
    soup = soup.find_all('td','tabla_campo_valor')
    if soup:
        linea, nom_parada, minutos, contador = [] , [], [], 0

        for i,td in enumerate(soup):    #Los multiplos de 3 van a ser
            if (i%3 == 0):
                linea.append(td.get_text().strip())
            elif (i%3 == 1):
                nom_parada.append(td.get_text().strip())
            elif (i%3 == 2):
                minutos.append(td.get_text().strip())
            contador +=1

        for i in range(0,int(contador/3)):
            print('Faltan ', minutos[i],' minutos para que llegue la linea '
                  ,linea[i],' a la parada',nom_parada[i],' numero: ',num_parada)
    else:
        print('No hay datos para esta parada')
