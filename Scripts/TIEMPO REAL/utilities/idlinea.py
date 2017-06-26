import pandas as pd

def retrieve_linea():
    df = pd.read_csv('..\..\Data\Web_crawling_T.Rober\lista_lineas_horarios.csv',
                     index_col = 'Unnamed: 0')



    id_ = input('Introduce la id_web asociada a la linea de la quieres obtener'+ \
                'info \n {0} \n'.format(df[['id_web','num_linea']]))
    return id_
