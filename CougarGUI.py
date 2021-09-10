import lasio
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sys import stdout
from openpyxl import Workbook
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits import mplot3d


# VARS CONSTS:
_VARS = {'window': False}

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", )
    return figure_canvas_agg



#Creacion de la funcion
def well_log(w):
    
    las_1 = lasio.read(w)
    # las_1.to_csv(stdout)
    df = las_1.df()
    df.reset_index(inplace =True)
    # df.to_excel("Registro_4.xlsx",sheet_name="Registro_4_Limpio",index=False)

    #Cambio de nombres para diferentes tipos de cabezales
    #Cambio de nombres de las columnas para diferentes tipos de cabezales
    if "ILD" in df:
        df = df.rename(columns={'ILD':'AT90'})
    if "DEPTH" in df:
        df = df.rename(columns={'DEPTH':'DEPTH:1'})
    if "DDLL" in df:
        df = df.rename(columns={'DDLL':'AT90'})
    if "RT" in df:
        df = df.rename(columns={'RT':'AT90'})
    if "GRGC" in df:
        df = df.rename(columns={'GRGC':'GR'})
    if "RHOZ" in df:
        df = df.rename(columns={'RHOZ':'DEN'})
    if "RHOB" in df:
        df = df.rename(columns={'RHOB':'DEN'})
    if ("NPHI") in df:
        df = df.rename(columns={'NPHI':'NEU'})
    if ("ILD") in df:
        df = df.rename(columns={'IDL':'AT90'})
    if "PDPE" in df:
        df = df.rename(columns={'PDPE':'PEF'})
    if "PEFZ" in df:
        df = df.rename(columns={'PEFZ':'PEF'})


    # Identifciación de los valores maximos y minimos del gamma ray
    GR_max = df['GR'].max()
    GR_min = df['GR'].min()

    #Identificación de shale del resto de litologías
    df.loc[df.GR>80,'Shale']= 0
    df.loc[df.GR<80,'Shale']= 1

    #Identificación de litologias mediante Neutron y Gamma Ray
    df["Lit_ND"] = (df["DEN"] - 1.95) - (1 - (5/3)*(df["NEU"]+0.15))

    # #Creación de la gráfica de litología
    # fig , axs = plt.subplots(figsize=(4,12))
    # plt.plot(df['Lit_ND'],df['DEPTH:1'])
    # plt.xlabel('Litología')
    # plt.ylabel('DEPTH:1')
    # plt.ylim(max(df['DEPTH:1']),min(df['DEPTH:1']))
    # # fig.savefig("DEPTH:1_vs_Lit_ND.png")

    #Creacion de la litología con curvas
    # Si es menor -0.03 Arenisca  2
    df.loc[df.Lit_ND < -0.03,'Litologia']= 2
    # Si esta en el rango de -0.03 a 0.03 limolita 3
    df.loc[df.Lit_ND >= -0.03,'Litologia']= 3
    #Si es mayor a 0.03 Dolomita 4
    df.loc[df.Lit_ND > 0.03,'Litologia']= 4


    df['Litologia'] = df['Litologia'] * df['Shale']

    # #Creación de la gráfica de litología
    fig , axs = plt.subplots(figsize=(3,10))
    plt.plot(df['Litologia'],df['DEPTH:1'])
    plt.grid()
    plt.xlabel('Litología')
    plt.ylabel('Depth')
    plt.ylim(max(df['DEPTH:1']),min(df['DEPTH:1']))
    plt.legend(['''Legend
                0 : Shale formation
                2 : Sandstone formation
                3 : Limolite formation
                4 : Dolomite formation'''])
    fig.savefig("Profundidad_litologia.png")
    

    #Asignacion de fila de matriz density
    df.loc[df.Litologia == 0,'Matrix_DEN']= 2.65
    df.loc[df.Litologia == 2,'Matrix_DEN']= 2.654
    df.loc[df.Litologia == 3,'Matrix_DEN']= 2.711
    df.loc[df.Litologia == 4,'Matrix_DEN']= 2.87

    ## Si hay toc

    if not "TOC" in df:
        df.loc[df.GR > 80,'TOC'] = ( 154.497 / df.DEN ) - 57.261
        df.loc[df['DEPTH:1'] < 6000,'TOC'] = np.nan
        
            #Calculo de m y Y del TOC
            # m_toc = 1 / ( ( 1 / 1.24 ) - ( 1 / df.Matrix_DEN ) )
            # y_toc = ( m_toc / df.Matrix_DEN )
            # df['TOC'] = ( m_toc / df.DEN ) + y_toc


    #Calculo de volumen de kerogeno
    VolK = (1.19 * df['TOC'] * df['DEN'])/( 100 * 1.24)

    #Correcion de densidad por TOC
    df.loc[df.TOC != 0,'DEN_K'] = (df['DEN'] - (1.24 * VolK )) / ( 1 - VolK)

    #Porosidad del kerogeno
    df['Poro_K'] = 0.2 * df['TOC'] * df['DEN']

    #Porosidad density total
    df.loc[df.DEN > 0,'Density'] = ((df['Matrix_DEN']-df['DEN'])/(df['Matrix_DEN']-1))
    df.loc[df.DEN_K > 0,'Density'] = ((df['Matrix_DEN']-df['DEN_K'])/(df['Matrix_DEN']-1)) + df['Poro_K']

    # Corrección de valores negativos
    df.loc[df.Density > 0 ,'DEN_TOTAL'] = ""
    df.loc[df.Density > 0 ,'DEN_TOTAL'] = df['Density']

    #Porosidad Total Neutron mas density
    df['Total_Poro'] = ( df['NEU'] + df['DEN_TOTAL'])/2

    #Calculo de la temperatura de la formacion
    df.loc[df['DEPTH:1'] <= 100,'Temperature'] = 75
    df.loc[df['DEPTH:1'] > 100,'Temperature'] = 75 + (0.74 * (df['DEPTH:1'] - 100) / 100)

    #Cálculo de la resistividad de la formación
    df.loc[df['DEPTH:1'] > 100,'RES_CORR'] = 0.2 * ( 75 + 6.77) / ( df['Temperature'] + 6.77 )

    #Calculo de Vclay
    GR = df['GR']
    IGR = (GR-GR_min)/(GR_max-GR_min)
    df['Vclay']= 1.7 - ( 3.38 - ( IGR + 0.7) ** 2 ) ** 0.5
    df.loc[df.Vclay > 0.7, 'Vclay'] = 0.7

    #Calculo de m y a
    df.loc[df.Vclay < 0.71, 'm'] = 1.08
    df.loc[df.Vclay < 0.35, 'm'] = 1.33
    df.loc[df.Vclay < 0.15, 'm'] = 1.54
    df.loc[df.Vclay < 0.05, 'm'] = 2

    #Calculo de a
    df.loc[df.Vclay < 0.71, 'a'] = 2.45
    df.loc[df.Vclay < 0.35, 'a'] = 1.65
    df.loc[df.Vclay < 0.15, 'a'] = 1.45
    df.loc[df.Vclay < 0.05, 'a'] = 1

    #identificar valores relacionados con el Gamma Ray
    GR = df[df.GR == GR_max ]
    resis_GR = GR['AT90'].max()
    poro_GR = GR['Total_Poro'].max()


    #Calculo de porosidad efectiva
    poro_efectiva = (df.DEN_TOTAL - poro_GR * df.Vclay ) * 100
    df.loc[poro_efectiva > 0, 'Poro_efective'] = poro_efectiva

    # Calculo de la Sw de agua de indonesia
    df['Sw'] = (( ( (df.Vclay ** ( 2 - df.Vclay)/resis_GR) ** (1 / 2) ) + ( (df.Poro_efective ** df.m ) / df.RES_CORR ) ** ( 1 / 2 ) ) ** 2  * df.AT90 ) ** ( -1 / 2 )


    # identificacion de zonas de interes
    df.loc[df.TOC > 2, 'Interest_Zone'] = df['TOC']

    fig , axs = plt.subplots(figsize=(3,10))
    plt.plot(df['Interest_Zone'],df['DEPTH:1'],'o')
    plt.grid()
    plt.xlabel('Interest_Zone')
    plt.ylabel('Depth')
    plt.ylim(max(df['DEPTH:1']),min(df['DEPTH:1']))
    plt.legend(['''Interest Zone'''])
    fig = plt.show()
    fig.savefig('Zona_interes.png')
    # Exportar a excel
    # df.to_excel('Registro.xlsx',sheet_name="Registro_1_Limpio",)

    
    #diseño del pozo en 3D
    v_hz = 3500
    
    r = np.arange(0,v_hz)
    
    x = r * (2**(1/2))
    y = r * (2**(1/2))
    z = - (v_iz / np.log(v_iz)) * np.log(np.arange(1,v_iz,(v_iz/v_hz)))

    ax = plt.axes(projection='3d')
    ax.plot3D(x, y, z)

    # Impresion de la gráfica y vista del archivo pandas
    # plt.show()
    

# __________________________________________________________________________________ #




sg.theme('GreenMono')
layout = [      
            [sg.Text('''Bienvenido al programa Cougar de identificacion de litologias, 
por favor en el siguiente espacio anexe la direccion del registro que usted desea leer
Al dar click en Cerrar se cerrara el proceso''')],
[sg.Text('Ingrese la direccion del archivo .las'),sg.InputText(),sg.FileBrowse()],
[sg.Button('Leer')],
                
            [
        sg.Column(layout_lito),
        sg.VSeperator(),
        sg.Column(layout_zone),
                    
]
]

#Creacion de la segunda caja
# layout_ = [
#     [sg.Text("Plot test")],
#     [sg.Canvas(key="-CANVAS-")],
# ]

### Creacion del Frontend
                
#Creacion de la ventana
window = sg.Window("Cougar",layout)



#Creacuon de un evento o accion
while True:
    event, values = window.read()
    
    if event == "Cerrar" or event == sg.WIN_CLOSED:
        break
    
    elif event == "Leer" or event == sg.WIN_CLOSED:
        w = values[0]
        well_log(w)
        
    elif event == "Exportar imagenes y excel":
        pass
        
window.close()