import pandas as pd

def retrieve_bus_line():
    df = pd.read_csv('..\..\Data\Web_crawling_T.Rober\lista_lineas_horarios.csv',
                     index_col = 'Unnamed: 0')



    id_ = input('Enter web_id associated to bus_line you want to obtain'+ \
                'info \n {0} \n'.format(df[['id_web','num_linea']]))
    return id_
