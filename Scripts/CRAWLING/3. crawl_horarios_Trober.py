from utilities.getting_soup_from_web import BSoup
import pandas as pd
#Obtenemos .csv con linea-codigos web para scrapear trayectos,
##paradas y horarios de cada linea

def listadoDF(url):
    lineas_horariosDF = pd.DataFrame(
        columns = ['id_web','nombre_linea','num_linea'])    

    soup = BSoup(url_lineas)
    table = soup.find('div',{'id':'div_lineas'})

    for inputs in table.find_all('input'):
        name, value = inputs['id'],inputs['value']
        labl = table.find('label',{'for':name}).text
        num_linea = labl.split('-')[0].strip()
        lineas_horariosDF = lineas_horariosDF.append(pd.DataFrame(
            {'id_web':value,'nombre_linea':labl,'num_linea':num_linea},
            index=[0]))
    return lineas_horariosDF

url_lineas = 'http://transportesrober.com:9055/websae/Transportes/'+ \
             'buscar_horarios.aspx'
listadoDF(url_lineas).to_csv('lista_lineas_horarios.csv')
