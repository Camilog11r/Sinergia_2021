import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sys import stdout
from openpyxl import Workbook
import numpy_financial as npf
import PySimpleGUI as sg



def economy(qi,qa,t,price_barrel,oportu_rate,ft,budget,area):
    
    oportu_rate = ( ( 1 + (oportu_rate / 100) ) ** ( 1 / 12 ) ) - 1
    ft = ft + 3500
    drill_well_cost = 2000000
        
    #Registro de variables fijas
    n = 0.9
    # sw = float(input("Ingrese el valor de la saturacion de agua"))
    # toc = float(input("Ingrese el valor promedio del porcentaje del TOC"))
    # den = float(input("Ingrese el valor de la densidad"))

    #Calculo D
    D = ( 1 / ( n * t ) ) * ( ( ( qi / qa ) ** n ) -1 )
    t_prod = [i for i in range (1,t + 2)]

    #Creacion de las listas de tiempo y produccion
    q = []
    for t_index in range (t+1):
        prod = qi * ( 1 + ( n * D * t_index )) ** (-1 / n )
        q.append(prod)

    #Creacion del dataframe curve y la curva de produccion +-50%
    curve = pd.DataFrame()

    curve['Tiempo (meses)'] = t_prod
    curve['Q'] = q

    # curve['Q +50%'] = curve['Q'] * 1.5
    # curve['Q -50%'] = curve['Q'] *0.5

    # curve.to_excel('curva_de_Produccion.xlsx',sheet_name="economia",)

    #Calculos economicos en funcion de la produccion 
    completion_cost = 850 * ft
    capex = drill_well_cost + completion_cost

    royalties = 0.08 * price_barrel
    taxes = 0.34 * price_barrel
    quality_penalty = 0.05 * price_barrel
    transport_price = 2
    administrative_cost = 2
    prod_cost_only = royalties + taxes + quality_penalty + transport_price + administrative_cost


    curve['Ingresos'] = curve['Q'] * price_barrel
    curve['Egresos'] = curve['Q'] * prod_cost_only
    curve['Flujo de Efectivo'] = curve['Ingresos'] - curve['Egresos']
    curve['Valor Presente'] = curve['Flujo de Efectivo'] /  (( 1 + oportu_rate ) ** curve['Tiempo (meses)'])
    curve = curve.append({'Tiempo (meses)' : 0 , 'Flujo de Efectivo': -capex, 'Valor Presente' : - capex }, ignore_index=True)


    #Cálculo de VPN
    van = curve['Valor Presente'].sum()
    print("VAN: ", van)

    #Cálculo de TIR
    cash_flow = curve['Flujo de Efectivo'].tolist()
    cash_flow.remove(-capex)
    cash_flow.insert(0,-capex)
    # print(cash_flow)
    irr = npf.irr(cash_flow)

    print("TIR:" ,irr)

    #PayBackTime________________________________
    cash_vpn = curve['Valor Presente'].tolist()
    cash_vpn.remove(-capex)
    cash_vpn.insert(0,-capex)



    accumulate = ( cash_vpn[0] + cash_vpn[1] )
    # print(cash_vpn[0])
    # print(accumulate)
    accumu = accumulate

    accumulate_1 = ( cash_vpn[0] + cash_vpn[1] )
    list_accumalte =[]
    list_accumalte.append(cash_vpn[0])
    list_accumalte.append(accumulate)

    # Creacion de lista
    for t_index in range(2,t+2) :
        accumu = accumu + cash_vpn[t_index]
        list_accumalte.append(accumu)

    # Número anterior
    for t_index in range(2,t+2) :
        accumulate = accumulate + cash_vpn[t_index]
        t_accumulate = t_index
        if accumulate < 0:
            break
        # print(accumulate)

    #Número siguiente
    for t_index in range(2,t+2) :
        accumulate_1 = accumulate_1 + cash_vpn[t_index]
        if accumulate_1 > 0:
            break
        # print(accumulate)

    pbt = round(( - accumulate / (- accumulate + accumulate_1) ) + t_accumulate,2)
    print("Pay Back Time", pbt)

    curve['Flujo acumulado en VP'] = list_accumalte

    #Grafica de flujo acumulado
    curve['Flujo acumulado en VP'].plot()
    plt.grid()
    plt.xticks()
    plt.yticks()


    #Grafica de flujo de caja
    fig , axs = plt.subplots(figsize=(4,12))
    plt.bar(curve['Tiempo (meses)'],curve['Flujo de Efectivo'])
    plt.grid()
    plt.xlabel('Meses')
    plt.ylabel('Flujo de Efectivo')
    plt.show()

    print(curve)

    # Exportar a excel
    curve.to_excel('Registro economico',sheet_name="Tablas")
    return df


#------------------------------------------------------------------------------
#Creacion de la interfaz grafica
layout = [
    [sg.Text("""Bienvenido a Leopard. Herramienta virtual para identificar la viabilidad de los poryectos economicos """)],
    [sg.Text('Ingrese la tasa mas alta de produccion registrado'),sg.Input()],
    [sg.Text('Ingrese la tasa de abandono de produccion '),sg.Input()],
    [sg.Text('Ingrese el tiempo de produccionde abandono'),sg.Input()],
    [sg.Text('Ingrese el precio del barril'),sg.Input()],
    [sg.Text('Ingrese el porcentaje (Valor de 0 a 100) referente a la tasa de oportunidad'),sg.Input()],
    [sg.Text('Ingrese la profundidad de la zona de interes'),sg.Input()],
    [sg.Text('Ingrese el presupuesto en dolares'),sg.Input()],
    [sg.Text('Ingrese el area'),sg.Input()],
    [sg.Button('Guardar'),sg.Button("Cancel")]
]



window = sg.Window('Get filename example', layout)
while True:
        event, values = window.read()
        if event == "Cancel" or event == sg.WIN_CLOSED:
            break
        if event == "Guardar": 
            qi = int(values[0])
            qa = int(values[1])
            t = int(values[2])
            price_barrel = int(values[3])
            oportu_rate = int(values[4])
            ft = int(values[5])
            budget = int(values[6])
            area = int(values[7])
            economy(qi,qa,t,price_barrel,oportu_rate,ft,budget,area)

event, values = window.read()
window.close()



    # Impresion de la gráfica y vista del archivo pandas
    # plt.show()
    # print(df)
