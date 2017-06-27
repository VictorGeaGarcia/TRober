import pandas as pd

from utilities.getting_soup_from_web import BSoup

def csv_scraping_codes(url_buslines):
    '''RETURNS A DF THAT POPULATE A CSV FILE WITH A LIST OF BUS LINES
       AND ITS CORRESPONDENT CODES FOR SCRAPING ROUTES, BUS STOPS AND
       TIMETABLES FOR EACH BUS LINE'''
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
csv_output_file = '..\..\Data\Web_crawling_T.Rober\lista_lineas_horarios.csv'
csv_scraping_codes(url_buslines).to_csv(csv_output_file)

