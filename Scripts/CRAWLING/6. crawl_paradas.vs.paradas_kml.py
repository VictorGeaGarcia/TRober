import pandas as pd
import sqlite3

def limpia_tildes_dim(row):
    '''WE CLEAN THE BUS_STOPS SO THAT THEY DONT CONTAIN WEIRD CHARACTERS
       NOR WEIRD NAMES SO THAT WE CAN MATCH EASILY BUS_STOPS CRAWLED
       FROM KML FILES AND THOSE IN T.ROBER WEBPAGE'''
    simbols_wrong = ['Av. ', 'Av.', 'Avda ', 'Avda. ', 'Avda.de ', 'Avda.',
                     'Sta M?', 'Santa M?', 'Cno', 'Ctra','D?a. M?','N.? S.?',
                     'Jose M?','mª','n.ª s.ª','gª','P.?', 'Arg?eta','Ni?os',
                     'C/']
    simbols_right = ['avenida ', 'avenida ', 'avenida ', 'avenida ',
                     'avenida de ','avenida ', 'santa maria ','santa maria ',
                     'camino ', 'carretera ', 'doctora maria ',
                     'nuestra señora', 'jose maria ', 'maria ',
                     'nuestra señora ','garcia ','paseo ','argueta ','niños ',
                     '']

    for k,v in zip(simbols_wrong,simbols_right):
        row = row.replace(k,v)
    row = row.strip().split()

    row = ' '.join(row)
    row = row.split('-')
    for n,i in enumerate(row):
        row[n] = row[n].strip()
    row = ' - '.join(row)
    row = row.lower()
    row = row.translate({ord('á'):'a',ord('é'):'e',ord('í'):'i',ord('ó'):'o',
                         ord('ú'):'u'})
    return row

def coordenadas(row):
    '''WE OBTAIN COORDINATES FOR THOSE BUS_STOPS FOUND IN KML FILE'''
    match = paradas_kml[['Lon','Lat']][paradas_kml.Name == row.paradas]
    if match.index.size == 0: #No ha habido match para la parada
        no_matchset.add(row.paradas)
         #No hay match, ponemos un 0 para que sea consistente con los
         #datos de la database
        return 0 , 0 
    else:
        yes_matchset.add(row.paradas)
        lon , lat = match.iloc[0].Lon , match.iloc[0].Lat
        return [lon , lat]

def main():
    '''DB POPULATION WITH COORDINATES FOR THOSE BUS_STOPS FOUND IN THE
       KML FILE'''

    #THIS HAS TO BE UPDATED TO WORK WITH THE NEW DATABASE CONTAINING
    #BOTH TIMETABLES AND BUS_STOPS 
    conn = sqlite3.connect('..\..\Data\Web_crawling_T.Rober\paradas_Trober.db')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    lineas_tablanombres = c.fetchall()

    lista_lineas = []
    for linea in lineas_tablanombres:
        lista_lineas.append(linea[0])

    for linea in lista_lineas:
        print(linea)
        paradasDF = pd.read_sql(
            sql = 'SELECT * FROM '+'{0}'.format(linea),con = conn)
        if not(paradasDF.empty):
            '''We make sure that we gathered data(
            otherwise it returns an error'''
            paradasDF['paradas'] = paradasDF.paradas.apply(limpia_tildes_dim)
            paradasDF['Lon'], paradasDF['Lat'] =  zip(*paradasDF.apply(
                coordenadas,axis=1))
            paradasDF = paradasDF [['paradas','transbordos','Lon','Lat']]
    ##  paradasDF.to_sql(
    ## '{}'.format(linea),con = conn,if_exists = 'replace',index=False)
    ## cursor.execute("ALTER TABLE "+'{}'.format(linea)+" ADD COLUMN lon REAL")
    ## cursor.execute("ALTER TABLE "+'{}'.format(linea)+" ADD COLUMN lat REAL")
    c.close()    
    conn.close()
    prompt = 'Number of stops without a match: '+str(len(no_matchset))
    prompt += '\nNumber of stops with a match: '+str(len(yes_matchset))
    return prompt
paradas_kml = '..\..\Data\Web_crawling_T.Rober\paradasporlinea_kml.csv'
paradas_kml = pd.read_csv(paradas_kml,index_col = 'Unnamed: 0')
paradas_kml = paradas_kml.drop_duplicates(subset = ['Name'])
paradas_kml = paradas_kml.drop('Linea',axis=1)
paradas_kml['Name'] = paradas_kml.Name.apply(limpia_tildes_dim)

no_matchset, yes_matchset = set(), set()

print(main())

