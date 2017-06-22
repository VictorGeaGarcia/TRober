import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

#############################################################################
#####CREAR ITERACION CON TODAS LAS LINEAS Y CORRER ESTO TAL CUAL ESTA########
#############################################################################

conn = sqlite3.connect('paradas_Trober.db')
c = conn.cursor()

listado_lineasDF = pd.read_csv('lista_lineas_horarios.csv',index_col=
                               'Unnamed: 0')
lineas = listado_lineasDF.id_web.values
no_info = []  #Lista para las lineas para las que no se va a obtener informacion

for linea in lineas:
    print('Trabajando en la linea: ',listado_lineasDF[listado_lineasDF.id_web == int(linea)].nombre_linea,'...')
    linea = str(linea)
    url = 'http://transportesrober.com:9055/websae/Transportes/linea.aspx?idlinea='+linea
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)

    soup = soup.find('div',{'id':'PanelHorario'})
    if (bool(soup)):#Control porque en algunos casos soup no tenia (div:id Panel horario)

        lista_trayectos = []  ##Creamos una lista con los nombres de los distintos trayectos para esa linea

        ###Control para asegurarnos que hay info de los distintos trayectos
        control = soup.find('span',{'class':'texto'})
        if not(bool(control)):
            trayectos = soup.find_all('td',{'class':'tablasubtitulo'})
            for i,trayecto in enumerate(trayectos):
                   
                nombre_tabla = 'L'+linea+'_'+trayecto.text.strip().split()[1]
                if ('-' in nombre_tabla) or ('.' in nombre_tabla):
                    nombre_tabla = 'L'+linea+'_'+'otro'
                                
                lista_trayectos.append(nombre_tabla)  ##Aqui para luego meter en la database los datos con sus
                                                          ##nombres de trayecto
            #Aqqui controlamos que los trayectos no tengan el mismo nombre, si no van a crear la misma tabla en
            #el sql y eso va a dar un problema
            if (len(lista_trayectos)>1):
                for i in range(1,len(lista_trayectos)):
                    if (lista_trayectos[i-1] == lista_trayectos[i]):
                        lista_trayectos[i] = lista_trayectos[1]+'otro'
                    if (len(lista_trayectos)>2) and (lista_trayectos[i-2] == lista_trayectos[i]):
                        lista_trayectos[i] = lista_trayectos[1]+'otro'
                        
            num_trayectos = len(soup.find_all('table',{'class':'tablabusqueda'}))
            trayectos = soup.find_all('table',{'class':'tablabusqueda'})

            for i,x in enumerate(trayectos):
                c.execute('CREATE TABLE '+'{0}'.format(lista_trayectos[i])+'(parada TEXT, transbordos TEXT)')                
                trayecto = x.find_all('tr',{'class':'tabla_campo_valor'})

                for parada in trayecto:
                    parada = parada.find_all('tr')
                    parada_ = parada[0].find('a',{'class':'texto'}).text
                    transbordos = []

                    for transbordo in parada[2].find_all('a',{'class':'texto'}):                        
                        transbordos.append(transbordo.text)
                    
                    transbordos_ = ' '.join(transbordos) ##PORQUE SQLITE3 NO COGE LISTS
                    c.execute('INSERT INTO '+'{0}'.format(lista_trayectos[i])+' VALUES (?,?)',(parada_,transbordos_))
                    conn.commit()
        else:
            print('No habia info para la linea: ', listado_lineasDF[listado_lineasDF.id_web == int(linea)].nombre_linea)
            no_info.append(listado_lineasDF[listado_lineasDF.id_web == int(linea)].loc[0,'nombre_linea'])
    else:
        print('No habia info para la linea: ', listado_lineasDF[listado_lineasDF.id_web == int(linea)].loc[0,'nombre_linea'])
        no_info.append(listado_lineasDF[listado_lineasDF.id_web == int(linea)].loc[0,'nombre_linea'])

c.close()
conn.close()
print(no_info)

