import numpy as np
import matplotlib.pyplot as plt

diff = 1/32 # longitud del paso
urow = 2/diff-1 # Cantidad de filas Ui
urow = ucol = int(urow) # Convert float to int
frow = fcol = urow + 2
eqMatrix = np.zeros([urow*fcol,urow*fcol]) # Matrix
bCol = np.zeros(urow*frow)
eqCont = 0

NumberTable = np.arange(1,urow*fcol+1) # Array with Ui and Fi
zerosrow = np.zeros(fcol) # Row of zeros
fxrow1 = np.arange(0,-1,-diff) # f(x), 0<x<1
fxrow2 = np.sort(fxrow1) # f(x), 1<x<2
if 1%diff == 0.0:
    fxrow = np.hstack((fxrow1,-1,fxrow2)) # f(x)
else:
    fxrow = np.hstack((fxrow1,fxrow2)) # f(x)
CoordTable = np.hstack((fxrow, NumberTable, zerosrow)) # Table with condiciones de contorno en filas extremas y numeros ordenados en el medio
CoordTable = CoordTable.reshape(frow,fcol) # Add 2 columns: Fi ---
#print(CoordTable)
for i in range(0,fcol): # Columns
    for j in range(1,urow+1): # Rows
        #print("col",i,"row",j)
        eqMatrix[eqCont,int(CoordTable[j,i])-1] += -4 # CENTRO
        if CoordTable[j-1,i] > 0 : # ARRIBA
            eqMatrix[eqCont, int(CoordTable[j-1,i])-1] += 1
        else:
            bCol[eqCont] += CoordTable[j-1,i]
        if CoordTable[j+1,i] > 0: #ABAJO
            eqMatrix[eqCont,int(CoordTable[j+1,i])-1] += 1
        if i == 0: #IZQUIERDA
            eqMatrix[eqCont,int(CoordTable[j,i+1])-1] += 2
        else:
            if i == fcol-1: #DERECHA
                eqMatrix[eqCont,int(CoordTable[j,i-1])-1] += 2
            else: #Medio
                eqMatrix[eqCont, int(CoordTable[j,i-1])-1] += 1
                eqMatrix[eqCont, int(CoordTable[j,i+1])-1] += 1
        eqCont += 1
solution = np.linalg.solve(eqMatrix,bCol) #Método 1
#np.dot(np.lingalg.inv(eqMatrix), bCol) # Método 2
#print(solution)
h= solution.reshape(int(2/diff+1)-2, int(2/diff+1)) # Paso de fila a matriz # Lo doy vuelta pq me devuelve la solución espejada respecto al plano y=1
Z = np.vstack([zerosrow, np.flipud(h), np.absolute(fxrow)]) # Anexo condiciones de contorno a la solucion obtenida
#print(Z)
x = np.arange(0, 2.01, diff) # PROBAR LINSPACE
y = np.arange(0, 2.01, diff) # PROBAR LINSPACE
X, Y = np.meshgrid(x,y)

# Create a 3D surface plot with x,y,z orthogonal axis:
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
# Create 1 3D subplot:
ax = fig.add_subplot(111, projection='3d')
# Add colormap
from matplotlib import cm
ax.plot_surface(X, Y, Z,cmap=cm.viridis,linewidth=0)
# Create x,y,z axis labels:
ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_zlabel('Z Axis')

plt.show()