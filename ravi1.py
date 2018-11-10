import matplotlib.pyplot as plt
import numpy as np
from math import e

meshdensity = 2
k=meshdensity
core = 1.0
dimension=100

grid=meshdensity*dimension

s11 = np.zeros([grid,grid])
s22 = np.zeros([grid,grid])
s12 = np.zeros([grid,grid])
H = np.zeros([grid,grid])

#print(s11)

nu = 0.44
sc = 48.0*(pow(e,9)*(3.16*(pow(e,-10))))/(2*np.pi*(1-nu))
bc = pow(e,-9)*0.361



for m in range(1,grid):
  for n in range(1,grid):
    if(m==grid/2):
      continue
    location=grid/2
    z=bc*(m-location)
    x=bc*(n-location)
    
    ts11=sc*(z*(3*(x*x)+(z*z)))/pow(((x*x)+(z*z)),2)
    ts22=sc*(z*((x*x)-(z*z)))/pow(((x*x)+(z*z)),2)
    ts33=sc*0.5*(ts11+ts22)
    
    ts12=sc*(x*((x*x)-(z*z)))/pow(((x*x)+(z*z)),2)
    
    H[m,n]=(ts11+ts22+ts33)/3
    
    s11[m,n]=ts11
    s22[m,n]=ts22
    s12[m,n]=ts12
    
#print(s11, s22, s12)
X = []
Y= []
i = 0
for i in range(0,grid):
    X.append(i)
    Y.append(i)


plt.axis([80,140,80,140])
#plt.contour(X, Y, s11, colors='black');
plt.contour(X, Y, s22, colors='black');
#plt.contour(X, Y, s11, colors='black');


plt.colorbar()
#ax.set_aspect('equal')

plt.show()
