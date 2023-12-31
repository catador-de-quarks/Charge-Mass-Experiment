# -*- coding: utf-8 -*-
"""Práctica

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gIUe9y4hlI6dkNlfCwUfXeDQfILD2kIk
"""

import numpy as np
import scipy
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

voltajes4 = list(range(100, 270, 10))
voltajes = list(range(140, 360, 10))

corrientes4 = [1.39,1.89,2.61,2.78,2.91,3.04,3.16,3.18,3.27,3.36,3.46,3.56,3.62,3.71,3.80,
               3.88,3.94]
corrientes6 = [1.85,1.95,2.03,2.10,2.16,2.24,2.25,2.31,2.37,2.41,2.48,2.53,2.60,2.64,2.69,2.72,2.77,
               2.83,2.87,2.91,2.96,3]
corrientes8 = [1.31,1.40,1.46,1.52,1.56,1.61,1.68,1.70,1.76,1.79,1.84,1.89,1.91,1.95,2.00,2.03,
               2.07,2.10,2.13,2.17,2.20,2.24]
corrientes10 = [1.03,1.08,1.13,1.19,1.23,1.27,1.32,1.36,1.40,1.43,1.48,1.50,1.53,1.56,1.60,1.62,
                1.64,1.68,1.71,1.73,1.75,1.77]

mu0 = scipy.constants.physical_constants["vacuum mag. permeability"][0]
cte = (4/5)**(3/2)
n = 154
R = 0.2

B = [(cte*mu0*n/R) * i for i in corrientes4]
em1 = [(2*voltajes4[i])/((0.02*0.02)*B[i]*B[i]) for i in range(len(voltajes4))] #Creación del arreglo para los valores de la relación carga masa

B6 = [(cte*mu0*n/R) * i for i in corrientes6]
em2 = [(2*voltajes[i])/((0.03*0.03)*B6[i]*B6[i]) for i in range(len(voltajes))]

B8 = [(cte*mu0*n/R) * i for i in corrientes8]
em3 = [(2*voltajes[i])/((0.04*0.04)*B8[i]*B8[i]) for i in range(len(voltajes))]

B10 = [(cte*mu0*n/R) * i for i in corrientes10]
em4 = [(2*voltajes[i])/((0.05*0.05)*B10[i]*B10[i]) for i in range(len(voltajes))]

plt.axhline(y=1.7588e11, color='r', linestyle='-')

xdata = np.asarray(corrientes4)
ydata = np.asarray(em1)
plt.plot(xdata, ydata, 'o')

xdata = np.asarray(corrientes6)
ydata = np.asarray(em2)
plt.plot(xdata, ydata, 'o')

xdata = np.asarray(corrientes8)
ydata = np.asarray(em3)
plt.plot(xdata, ydata, 'o')

xdata = np.asarray(corrientes10)
ydata = np.asarray(em4)
plt.plot(xdata, ydata, 'o')

#Cálculo del valor medio de em
em=0
for i in range(2, len(voltajes4)):
  em=em+em1[i]
for i in range(len(voltajes)):
  em=em+em2[i]+em3[i]+em4[i]

em=em/(3*len(voltajes)+len(voltajes4)-2)

print(em)

#Aquí vamos a hace ajustes para rectas con cada uno de los set de datos. Vamos a ajustar a una recta de la forma B^2=(m/e)(2U/r^2).
B2 = [B[i]**2 for i in range(2, len(B))]
B62 = [B6[i]**2 for i in range(len(B6))]
B82 = [B8[i]**2 for i in range(len(B8))]
B102 = [B10[i]**2 for i in range(len(B10))]

abs4 = [2*voltajes4[i]/(0.02**2) for i in range(2, len(voltajes4))]
abs6 = [2*voltajes[i]/(0.03**2) for i in range(len(voltajes))]
abs8 = [2*voltajes[i]/(0.04**2) for i in range(len(voltajes))]
abs10 = [2*voltajes[i]/(0.05**2) for i in range(len(voltajes))]

coef1 = np.polyfit(abs4, B2, 1)
coef2 = np.polyfit(abs6, B62, 1)
coef3 = np.polyfit(abs8, B82, 1)
coef4 = np.polyfit(abs10, B102, 1)

residuals1 = B2 - np.polyval(coef1, abs4)
residuals2 = B62 - np.polyval(coef2, abs6)
residuals3 = B82 - np.polyval(coef3, abs8)
residuals4 = B102 - np.polyval(coef4, abs10)
n1=len(B2)
n2=len(B62)

Dm1=np.sqrt(sum(residuals1**2) / ((n1-2) * sum((abs4 - np.mean(abs4))**2)))
Dm2=np.sqrt(sum(residuals2**2) / ((n2-2) * sum((abs6 - np.mean(abs6))**2)))
Dm3=np.sqrt(sum(residuals3**2) / ((n2-2) * sum((abs8 - np.mean(abs8))**2)))
Dm4=np.sqrt(sum(residuals4**2) / ((n2-2) * sum((abs10 - np.mean(abs10))**2)))

Dem1=Dm1/(coef1[0]**2)
Dem2=Dm2/(coef2[0]**2)
Dem3=Dm3/(coef3[0]**2)
Dem4=Dm4/(coef4[0]**2)
sumw=1/Dem1**2+1/Dem2**2+1/Dem3**2+1/Dem4**2
Dem=np.sqrt(1/sumw)
empesado=(1/(coef1[0]*Dem1**2)+1/(coef2[0]*Dem2**2)+1/(coef3[0]*Dem3**2)+1/(coef4[0]*Dem4**2))/sumw

print(empesado,"\u00B1",Dem)
print("e/m: {:.2e} ± {:.3e}".format(empesado, Dem))

#Ejemplo de la banda de confianza

import numpy as np
import seaborn as sns
import pandas as pd

# Generate some random data for demonstration
np.random.seed(0)
x = np.random.randn(100)
y = 2 * x + np.random.randn(100)

# Create a DataFrame from the data
data = {"x": x, "y": y}
df = pd.DataFrame(data)

# Plot the regression line with confidence band using lmplot
sns.lmplot(x="x", y="y", data=df, ci=95)

plt.xlabel('X')
plt.ylabel('Y')
plt.show()

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Generate some random data for demonstration
np.random.seed(0)
x = np.arange(1, 20)
y = np.random.randn(19)
error = abs(np.random.randn(19) * 0.5)
error2=error*2

# Create a DataFrame from the data
data = {"x": x, "y": y, "error": error}
df = pd.DataFrame(data)

# Plot the scatter plot with confidence band and error bars
sns.lmplot(x="x", y="y", data=df, ci=95)
plt.errorbar(x, y, xerr=error2, yerr=error, fmt='none', capsize=4, color='gray')

plt.xlabel('X')
plt.ylabel('Y')
plt.show()

# Gráficas de los ajustes con bandas de confianza y todo

#Declaración de variables e incertidumbres
xer1=np.zeros(len(abs4))
yer1=np.zeros(len(B2))
xer2=np.zeros(len(abs6))
yer2=np.zeros(len(B62))
xer3=np.zeros(len(abs8))
yer3=np.zeros(len(B82))
xer4=np.zeros(len(abs10))
yer4=np.zeros(len(B102))

DFr1=0.01
DRr1=0.001/0.02
DFr2=0.01
DRr2=0.001/0.03
DFr3=0.02
DRr3=0.001/0.04
DFr4=0.02
DRr4=0.001/0.05

Di=0.01

def DV(V):
  if V<270:
    return 1
  else:
    return 2

#Propagación de errores
for i in range(len(abs4)):
  xer1[i]=abs4[i]*np.sqrt((DV(voltajes4[i])/voltajes4[i])**2+(2*DRr1)**2)
  yer1[i]=B2[i]*2*np.sqrt((Di/corrientes4[i])**2+(DFr1)**2)

for i in range(len(abs6)):
  xer2[i]=abs6[i]*np.sqrt((DV(voltajes[i])/voltajes[i])**2+(2*DRr2)**2)
  yer2[i]=B62[i]*2*np.sqrt((Di/corrientes6[i])**2+(DFr2)**2)
  xer3[i]=abs8[i]*np.sqrt((DV(voltajes[i])/voltajes[i])**2+(2*DRr3)**2)
  yer3[i]=B82[i]*2*np.sqrt((Di/corrientes8[i])**2+(DFr3)**2)
  xer4[i]=abs10[i]*np.sqrt((DV(voltajes[i])/voltajes[i])**2+(2*DRr4)**2)
  yer4[i]=B102[i]*2*np.sqrt((Di/corrientes10[i])**2+(DFr4)**2)

#Almacenar datos
data1 = {"x": abs4, "y": B2}
df1 = pd.DataFrame(data1)
data2 = {"x": abs6, "y": B62}
df2 = pd.DataFrame(data2)
data3 = {"x": abs8, "y": B82}
df3 = pd.DataFrame(data3)
data4 = {"x": abs10, "y": B102}
df4 = pd.DataFrame(data4)

# Plot the regression line with confidence band using lmplot
sns.lmplot(x="x", y="y", data=df1, ci=95)
plt.errorbar(abs4, B2, xerr=xer1, yerr=yer1, fmt='none', capsize=4, color='gray', alpha=0.5)
plt.xlabel('X [$V/m^2$]')
plt.ylabel('$B^2$ [$T^2$]')
plt.legend(['Datos', 'Ajuste', 'Banda de confianza a 95%', 'Barras de error'])
plt.ticklabel_format(style='sci', axis='both', scilimits=(0,0))
plt.show()

sns.lmplot(x="x", y="y", data=df2, ci=95, legend=1)
plt.errorbar(abs6, B62, xerr=xer2, yerr=yer2, fmt='none', capsize=4, color='gray', alpha=0.5)
plt.xlabel('X [$V/m^2$]')
plt.ylabel('$B^2$ [$T^2$]')
plt.legend(['Datos', 'Ajuste', 'Banda de confianza a 95%', 'Barras de error'])
plt.ticklabel_format(style='sci', axis='both', scilimits=(0,0))
plt.show()

sns.lmplot(x="x", y="y", data=df3, ci=95)
plt.errorbar(abs8, B82, xerr=xer3, yerr=yer3, fmt='none', capsize=4, color='gray', alpha=0.5)
plt.xlabel('X [$V/m^2$]')
plt.ylabel('$B^2$ [$T^2$]')
plt.legend(['Datos', 'Ajuste', 'Banda de confianza a 95%', 'Barras de error'])
plt.ticklabel_format(style='sci', axis='both', scilimits=(0,0))
plt.show()

sns.lmplot(x="x", y="y", data=df4, ci=95)
plt.errorbar(abs10, B102, xerr=xer4, yerr=yer4, fmt='none', capsize=4, color='gray', alpha=0.5)
plt.xlabel('X [$V/m^2$]')
plt.ylabel('$B^2$ [$T^2$]')
plt.legend(['Datos', 'Ajuste', 'Banda de confianza a 95%', 'Barras de error'])
plt.ticklabel_format(style='sci', axis='both', scilimits=(0,0))
plt.show()