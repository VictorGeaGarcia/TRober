from utilities.getting_soup_from_web import BSoup
import pandas as pd

'''Returns .csv file with list of Bus Lines and its correspondent codes for
scraping Routes, Bus Stops and Timetables for each Bus Line'''

def csv_scraping_codes(url_buslines):
    lines_timetablesDF = pd.DataFrame(
        columns = ['id_web','nombre_linea','num_linea'])    

    soup = BSoup(url_buslines)
    table = soup.find('div',{'id':'div_lineas'})

    for inputs in table.find_all('input'):
        name, value = inputs['id'],inputs['value']
        label = table.find('label',{'for':name}).text
        line_number = label.split('-')[0].strip()
        lines_timetablesDF = lines_timetablesDF.append(pd.DataFrame(
            {'id_web':value,'nombre_linea':label,'num_linea':line_number},
            index=[0]))
    return lines_timetablesDF

url_buslines = 'http://transportesrober.com:9055/websae/Transportes/'+ \
             'buscar_horarios.aspx'
csv_scraping_codes(url_buslines).to_csv('lista_lineas_horarios.csv')

