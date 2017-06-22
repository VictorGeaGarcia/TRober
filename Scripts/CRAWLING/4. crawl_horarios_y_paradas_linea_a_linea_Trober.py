from utilities.getting_soup_from_web import BSoup
import pandas as pd
import sqlite3

#### CREAMOS 2 BASES DE DATOS, UNA CON LINEAS Y OTRA CON HORARIOS DE CADA LINEA
def funcion_database(id_web,num_linea,conn_horas,conn_paradas):
    no_entrado_horas   = [] #por si no entra,sabemos en que linea no ha entrado
    no_entrado_paradas = [] #por si no entra,sabemos linea no ha entrado
    
    for id_,nombre in zip(id_web,num_linea):
        trayectos = []
        url_horas = 'http://transportesrober.com:9055/websae/Transportes/horar'+ \
                    'io.aspx?id={0}&tipo=L&nombre={1}&fecha=17/02/2017&desde_ho'+ \
                    'rario=si'.format(id_,nombre)
        soup = BSoup(url_horas).find('div',{'id':'PanelHorario'})
        
        if (bool(soup)):     
            trayectos = soup.find_all('td',{'class':'tablacabecera'})
            for i,trayecto in enumerate(trayectos):
                horasDF   = pd.DataFrame(columns = ['Linea','Trayecto','Horas'])
                nombre_tabla = '{}'.format(nombre)+'_'+ \
                               '_'.join(trayecto.text.strip().split())
                nombre_tabla = nombre_tabla.replace('-','').replace('__','_').replace(' ','')
                tabla_horarios = soup.find_all('table')[2+i]

                filas = tabla_horarios.find_all('tr')
                tr_horas = []
                for fila in filas:
                    tr_horas.extend(fila.text.split(':',1)[1].split(','))
##                tr_horas = ' '.join(tr_horas)
                #data = [[nombre,nombre_tabla,tr_horas]
                horasDF = horasDF.append(pd.DataFrame({'Linea':nombre,'Trayecto':nombre_tabla,'Horas':tr_horas},columns=['Linea','Trayecto','Horas']))
                
                horasDF.to_sql(nombre_tabla,conn_horas,index=False)
                conn_horas.commit()
        else: 
            no_entrado_horas.append(nombre)

        ##AHORA VAMOS CON LAS PARADAS, MANTENIENDO LA MISMA LISTA DE TRAYECTOS
        url_paradas = 'http://transportesrober.com:9055/websae/Transportes/'+ \
                      'linea.aspx?idlinea='+str(id_)
        soup = BSoup(url_paradas)
        if (bool(soup) & bool(trayectos)):
            for i,trayecto in enumerate(trayectos):
                paradasDF = pd.DataFrame(columns = ['parada','transbordos'])
            
                nombre_tabla = '{}'.format(nombre)+'_'+\
                               '_'.join(trayecto.text.strip().split())
                nombre_tabla = nombre_tabla.replace(
                    '-','').replace('__','_').replace(' ','')                
                trayecto = soup.find_all('tr',{'class':'tabla_campo_valor'})

                for parada in trayecto:
                    paradas = parada.find_all('tr')
                    parada = paradas[0].find('a',{'class':'texto'}).text
                    transbordos = []

                    for transbordo in paradas[2].find_all(
                        'a',{'class':'texto'}):                        
                        transbordos.append(transbordo.text)
                    
                    transbordos = ' '.join(transbordos)

                    paradasDF = paradasDF.append(
                        pd.DataFrame(data = [[parada,transbordos]],
                                     columns=['parada','transbordos']))
                paradasDF.to_sql(nombre_tabla,conn_paradas,index=False)
                conn_paradas.commit()
        else: 
            no_entrado_paradas.append(nombre)


def databases(id_web,num_linea):
    conn_horas = sqlite3.connect('horarios_lineas_Trober.db')
    conn_paradas = sqlite3.connect('paradas_Trober.db')
    
    funcion_database(id_web,num_linea,conn_horas,conn_paradas)
    
    conn_horas.close()
    conn_paradas.close()

listado_lineasDF = pd.read_csv('lista_lineas_horarios.csv',
                               index_col = 'Unnamed: 0')
listado_lineasDF = listado_lineasDF.reset_index(drop=True)

id_web = listado_lineasDF.id_web.values
num_linea = listado_lineasDF.num_linea.values
databases(id_web,num_linea)
