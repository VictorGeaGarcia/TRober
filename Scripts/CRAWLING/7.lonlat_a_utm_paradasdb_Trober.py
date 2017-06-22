import pandas as pd
import sqlite3
import pyproj

def coordgeo_a_utm(row):
    x1,x2 = row.Lon, row.Lat
    p1,p2 = pyproj.Proj(proj = 'lonlat', datum = 'WGS84'),pyproj.Proj(proj = 'utm', zone = 30, datum = 'WGS84')
    return pyproj.transform(p1,p2,x1,x2)



conn = sqlite3.connect('paradas_Trober.db')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
lineas_tablanombres = c.fetchall()

lista_lineas = []
for linea in lineas_tablanombres:
    lista_lineas.append(linea[0])

for linea in lista_lineas:
    paradasDF = pd.read_sql(sql = 'SELECT * FROM '+'{0}'.format(linea),con = conn)
    paradasDF ['Lon_utm'],paradasDF ['Lat_utm'] =zip(*paradasDF.apply(coordgeo_a_utm,axis=1))
##    paradasDF = paradasDF [['paradas','transbordos','Lon','Lat']]
##    print(paradasDF)
    paradasDF.to_sql('{}'.format(linea),con = conn,if_exists = 'replace',index=False)
