import pandas as pd
import sqlite3

###ASEGURARNOS QUE NO HAY TILDES EN NINGUNO DE LOS DOS, Y SI NO ELIMINARLAS

def limpia_tildes_dim(row):
##  Los de avenida funcionan regular, los simbolos raros no los pilla (Nª...=,
##  Los que sigan faltando mas adelante podriamos buscarlos en OSM  
    row = row.replace('Av. ','avenida ')
    row = row.replace('Av.','avenida ')
    row = row.replace('Avda ','avenida ')
    row = row.replace('Avda. ','avenida ')
    row = row.replace('Avda.de ','avenida de ')
    row = row.replace('Avda.','avenida ')
    row = row.replace('Sta M?','santa maria ')
    row = row.replace('Santa M?','santa maria ')
    row = row.replace('Cno','camino ')
    row = row.replace('Ctra','carretera ')
    row = row.replace('D?a. M?','doctora maria ')
    row = row.replace('N.? S.?','nuestra señora')
    row = row.replace('Jose M?','jose maria ')
    row = row.replace('mª','maria ')
    row = row.replace('n.ª s.ª','nuestra señora ')
    row = row.replace('gª','garcia ')
    row = row.replace('P.?','paseo ')
    row = row.replace('Arg?eta','argueta ')
    row = row.replace('Ni?os','niños ')
    row = row.replace('C/','')
    row = row.strip().split()
##  Aqui se podrian meter un par de iteraciones como esta, pero usando una lista adicional que luego
##  mantendriamos como row.   
##    for i,x in enumerate(row):
##        row[i] = x.strip()
    row = ' '.join(row)
    row = row.split('-')
    for n,i in enumerate(row):
        row[n] = row[n].strip()
    row = ' - '.join(row)
    row = row.lower()
    row = row.translate({ord('á'):'a',ord('é'):'e',ord('í'):'i',ord('ó'):'o',ord('ú'):'u'})
    return row

paradas_kml = pd.read_csv('/home/vilgegar/Documents/Proyecto SETIC/Sistema Integral/DBs&CSVs.../paradasporlinea_kml.csv',index_col = 'Unnamed: 0')
paradas_kml = paradas_kml.drop_duplicates(subset = ['Name']).drop('Linea',axis=1)
paradas_kml['Name'] = paradas_kml.Name.apply(limpia_tildes_dim)   ##ESto quiza no sea muy conveniente
                                                   ##hacerlo llamando a la nueva columna igual que a la vieja

no_matchset = set()

def coordenadas(row):
    match = paradas_kml[['Lon','Lat']][paradas_kml.Name == row.paradas]
    if match.index.size == 0: #No ha habido match para la parada
        no_matchset.add(row.paradas)
        return 0 , 0  #No hay match, ponemos un 0 para que sea consistente con los datos de la database
    else:
        lon , lat = match.iloc[0].Lon , match.iloc[0].Lat
        return lon , lat

conn = sqlite3.connect('paradas_Trober.db')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
lineas_tablanombres = c.fetchall()

lista_lineas = []
for linea in lineas_tablanombres:
    lista_lineas.append(linea[0])

for linea in lista_lineas:
    paradasDF = pd.read_sql(sql = 'SELECT * FROM '+'{0}'.format(linea),con = conn)
    paradasDF['paradas'] = paradasDF.parada.apply(limpia_tildes_dim)
    paradasDF['Lon'],paradasDF['Lat'] = zip(*paradasDF.apply(coordenadas,axis=1))
    paradasDF = paradasDF [['paradas','transbordos','Lon','Lat']]
    paradasDF.to_sql('{}'.format(linea),con = conn,if_exists = 'replace',index=False)
##    cursor.execute("ALTER TABLE "+'{}'.format(linea)+" ADD COLUMN lon REAL")
##    cursor.execute("ALTER TABLE "+'{}'.format(linea)+" ADD COLUMN lat REAL")
    
c.close()    
conn.close()

## Aqui abajo estan la lista de las lineas para las que no hay match
i = 0
for parada in no_matchset:
##    print(parada)
    i += 1
##print(i)
