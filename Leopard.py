import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sys import stdout
from openpyxl import Workbook

#Registro de variables fijas
n = 0.9

print("""
Bienvenido a Leopard, por favor ingrese las caracteristicas a los pozos asociados 
      """)
# sw = float(input("Ingrese el valor de la saturacion de agua"))
# toc = float(input("Ingrese el valor promedio del porcentaje del TOC"))
# den = float(input("Ingrese el valor de la densidad"))
qi = int(input('Ingrese la tasa de produccion mas alta: '))
qa = int(input('Ingrese el valor de tasa de producción de abanandono: '))
t = int(input('Ingrese tiempo de abandono: '))

#Calculo D
D = ( 1 / ( n * t ) ) * ( ( ( qi / qa ) ** n ) -1 )
t_prod = [i for i in range (t + 1)]

#Creacion de las listas de tiempo y produccion
q = []
for t_index in range (t+1):
    prod = qi * ( 1 + ( n * D * t_index )) ** (-1 / n )
    q.append(prod)


#Creacion del dataframe curve y la curva de produccion +-50%
curve = pd.DataFrame()
curve['Q'] = q
curve['Q +50%'] = curve['Q'] * 1.5
curve['Q -50%'] = curve['Q'] *0.5

curve.plot()
plt.grid()


#Calculos economicos en funcion de la produccion 
price_barrel = float ( input("Ingrese el precio del barril en dolares: "))
oportu_rate = float( input("Ingrese el porcentaje de tasa de oportunidad")) / 100
price_barrel = float ( input("Ingrese el precio del barril en dolares: "))
oportu_rate = float( input("Ingrese el porcentaje de tasa de oportunidad")) / 100
ft = float( input(" Ingrese la profundidad de la zona de interes mostrada de funetes externas o de Cougar")) + 3500
drill_well_cost = 2000000
completion_cost = 850 * ft
capex = drill_well_cost + completion_cost
economy = pd.DataFrame()
capex_data = {
    'Ingresos': 0 ,
    'Egresos': capex
}
royalties = 0.08 * price_barrel
taxes = 0.34 * price_barrel
quality_penalty = 0.05 * price_barrel
transport_price = 2
administrative_cost = 2
prod_cost_only = royalties + taxes + quality_penalty + transport_price + administrative_cost

economy['Ingresos'] = curve['Q'] * price_barrel
economy['Egresos'] = curve['Q'] * prod_cost_only

economy = economy.append(capex_data, ignore_index=True)

economy['Flujo de efectivo'] = economy['Ingresos'] - economy['Egresos']

economy







# Exportar a excel
# df.to_excel('Registro.xlsx',sheet_name="Registro_1_Limpio",)

# Impresion de la gráfica y vista del archivo pandas
# plt.show()
# print(df)