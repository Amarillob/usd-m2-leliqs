# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 21:01:44 2023

@author: Brian
"""
"""
Sources:
(millones de pesos) leliq: https://www.bcra.gob.ar/PublicacionesEstadisticas/Principales_variables_datos.asp?serie=7926&detalle=LELIQ%20saldos%20(en%20millones%20de%20pesos)    
(millones de pesos) agregados monetarios https://datos.gob.ar/dataset/sspm-series-historicas-estadisticas-monetarias/archivo/sspm_174.1    
    

"""
import os 
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt


#directoty setting
directory = "C:/Users\Brian\Desktop\BCRA"
os.chdir(directory)


db_names = ["agregados-monetarios.csv", "base_monetaria_seriehistorica.xlsx",
            "DOLAR MEP - Cotizaciones historicas.csv", "saldos_leliq_seirehistorica.xlsx"]

# import db
df = [pd.read_csv (db_names[0]),pd.read_excel(db_names[1]),
      pd.read_csv(db_names[2]),pd.read_excel(db_names[3]) ] 




#%% agregados_monetarios filtered by dates
agregados_monetarios = pd.DataFrame({
    "date": [   df[0]["indice_tiempo"][i]  for i in   range(247)   ],
    "value": [   df[0]["agregados_monetarios_totales_m2"][i]  for i in   range(247)   ]           
})



#%% base_monetaria_seriehistorica filtered by dates
# df[1]
dates = df[1]["Fecha"]

dates_moth = [date.month for date in dates]
dates_index = dates.index

index_selected = [0] #select each month fist date
for index in dates_index:
    if index != 0:
        index_previous = index - 1
        if dates_moth[index] != dates_moth[index_previous]:
            index_selected.append(index)
        
base_monetaria_seriehistorica = pd.DataFrame({
    "date": [   df[1]["Fecha"][index]       for index in index_selected],
    "value": [   df[1]["Valor"][index]       for index in index_selected]
})

        
#%% Dolar MEP filtered by dates     

df[2]["fecha"] =  [datetime.strptime(date, '%Y-%m-%d')         
                   for date in df[2]["fecha"]     ]



dates = df[2]["fecha"]

dates_moth = [date.month for date in dates]
dates_index = dates.index

index_selected = [0] #select each month fist date
for index in dates_index:
    if index != 0:
        index_previous = index - 1
        if dates_moth[index] != dates_moth[index_previous]:
            index_selected.append(index)
    


        
dolar_MEP = pd.DataFrame({
    "date": [   df[2]["fecha"][index]       for index in index_selected],
    "value": [   df[2]["ultimo"][index]       for index in index_selected]
})


#%% leliqs filtered by dates

dates = df[3]["Fecha"]

dates_moth = [date.month for date in dates]
dates_index = dates.index

index_selected = [0] #select each month fist date
for index in dates_index:
    if index != 0:
        index_previous = index - 1
        if dates_moth[index] != dates_moth[index_previous]:
            index_selected.append(index)
        
leliqs = pd.DataFrame({
    "date": [   df[3]["Fecha"][index]       for index in index_selected],
    "value": [   df[3]["Valor"][index]       for index in index_selected]
})


#%% keeping only

db = {"leliqs": leliqs,
      "dolar_MEP": dolar_MEP,
      "agregados_monetarios": agregados_monetarios}



# October 2018 to July 2023
db = {"agregados_monetarios": agregados_monetarios.iloc[189:247].reset_index(drop=True),
      "leliqs": leliqs.iloc[9:67].reset_index(drop=True),
      "dolar_MEP": dolar_MEP[0:58].reset_index(drop=True)
      }



# m2masleliqs
length = db["agregados_monetarios"].shape[0]

#creo la variable
m2masleliqs = [
    
               db["agregados_monetarios"]["value"].values[i]     
               +
               db["leliqs"]["value"].values[i]
               
               for i in range(length)
               
               ]

#creo el df        
db_m2masleliqs = pd.DataFrame({
    "date": list(   db["agregados_monetarios"]["date"].values   )  ,
    "value": m2masleliqs
})
                                                      

#agrego el df
db["m2masleliqs"] = db_m2masleliqs



for data_drame_name in db.keys():
    data_frame = db[data_drame_name]
    first_value = data_frame["value"][0]
    data_frame["value_standarized"] = [
        value/first_value   for value in data_frame["value"]    ]                                  
    



# graph
plt.figure()
plt.plot(   db["dolar_MEP"]["date"]    ,     db["m2masleliqs"]["value_standarized"]  , label = "MEP"   )
plt.plot(   db["dolar_MEP"]["date"]    ,     db["dolar_MEP"]["value_standarized"] , label = "M2+LELIQS"    )
plt.legend()



# porcentaje
porcentaje = db["dolar_MEP"]["value_standarized"]/db["m2masleliqs"]["value_standarized"]
plt.plot(   db["dolar_MEP"]["date"]    ,    porcentaje , label = "Porcentaje"   )




# Suponiendo que el equilibrio es 1.3, ¿cuanto tiene que ser al 1 de Julio
# valor del dolar en el dalo el ultimo valor de mb2 + leliqs? 
ponderador =   1.3 * db["m2masleliqs"]["value_standarized"][57]   
w = ponderador

MEP_equilibrip_lp = w   *    db["dolar_MEP"]["value"][0]
print(MEP_equilibrip_lp)

MEP_actually = db["dolar_MEP"]["value"][57]



ratio = MEP_equilibrip_lp/MEP_actually    #devaluacion para equilibrio
print(ratio)



current_date_equilibrium_mep = 540*ratio      #valor de equilbrio mep
print(current_date_equilibrium_mep)

# SUPONIENDO QUE EL MEP Y EL BLUE ESTABAN EN EQUILIBRIO
current_date_equilibrium_blue = 600*ratio      #valor de equilbrio blue
print(current_date_equilibrium_blue)












