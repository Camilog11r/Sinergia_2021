import lasio
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sys import stdout
from openpyxl import Workbook


w1 = r'.\DATOS_EDITADOS\SNRG-0001_FINAL.las'
w2 = r'./Well_Logging/SNRG-0002_basic_logs.las'
w3 = r'./Well_Logging/SNRG-0003_basic_logs.las'
w4 = r'./Well_Logging/SNRG-0004_basic_logs.las'

las_1 = lasio.read(w1)
# las_1.to_csv(stdout)
df = las_1.df()
df.reset_index(inplace =True)
# df.to_excel("Registro_4.xlsx",sheet_name="Registro_4_Limpio",index=False)

#Cambio de nombres para diferentes tipos de cabezales
if "GRGC" in df:
    df = df.rename(columns={'GRGC':'GR'})
if ("RHOB" or "RHOZ") in df:
    df = df.rename(columns={'RHOB':'DEN'})
    df = df.rename(columns={'RHOZ':'DEN'})
if ("NPHI") in df:
    df = df.rename(columns={'NPHI':'NEU'})
if ("DDLL" or "AT90" or "RT" or "ILD") in df:
    df = df.rename(columns={'DDLL':'AT90'})
    df = df.rename(columns={'AT90':'AT90'})
    df = df.rename(columns={'RT':'AT90'})
    df = df.rename(columns={'IDL':'AT90'})
if ("PDPE" or "PEFZ") in df:
    df = df.rename(columns={'PDPE':'PEF'})
    df = df.rename(columns={'PEFZ':'PEF'})

# Identifciación de los valores maximos y minimos del gamma ray
GR_max = df['GR'].max()
GR_min = df['GR'].min()

#Identificación de shale del resto de litologías
df.loc[df.GR>80,'Shale']= 0
df.loc[df.GR<80,'Shale']= 1

#Identificación de litologias mediante Neutron y density con gamma ray
df["Lit"] = (df["DEN"] - 1.95) - (1 - (5/3)*(df["NEU"]+0.15))

#Creación de la gráfica de litología
fig , axs = plt.subplots(figsize=(4,12))
plt.plot(df['Lit'],df['DEPTH'])
plt.xlabel('Litología')
plt.ylabel('Profundidad')
plt.ylim(max(df['DEPTH']),min(df['DEPTH']))
plt.show()

# fig.savefig("DEPTH_vs_Lit_ND.png")

#Creacion de la litología con curvas
#Si es mayor a 0.03 Dolomita 4
df.loc[df.Lit_ND>0.03,'Litologia']= 4
#Si es menor -0.03 Arenisca  2
df.loc[df.Lit_ND < -0.03,'Litologia']= 2
#Si esta en el rango de -0.03 a 0.03 limolita 3
df.loc[(df.Lit_ND >= -0.03 and df.Lit_ND <= -0.03) ,'Litologia']= 3
print(df)

# #Creación de la gráfica de litología
# fig , axs = plt.subplots(figsize=(4,12))
# plt.plot(df['Litologia'],df['DEPTH'])
# plt.xlabel('Litología')
# plt.ylabel('Depth')
# plt.ylim(max(df['DEPTH']),min(df['DEPTH']))
# fig.savefig("DEPTH_vs_Lit_ND.png")

# df.to_excel('registro_prueba.xlsx',sheet_name='prueba',index=False)