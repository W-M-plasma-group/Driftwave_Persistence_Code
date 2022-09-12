import matplotlib.pyplot as plt
# import xbout as xb
# from xbout import open_boutdataset
import numpy as np
import gudhi as gd
from matplotlib import pyplot
import xarray as xr
import netCDF4 as cdf
import scipy as sp
# import os

def get_betti(p):
  b0=[];y1=[];b1=[];y2=[];b2=[];y3=[]
  for i in range(len(p)):
    if p[i][0]==0:
      b0.append(p[i][1][0])
      y1.append(p[i][1][1])
    elif p[i][0]==1:
      b1.append(p[i][1][0])
      y2.append(p[i][1][1])
    else:
      b2.append(p[i][1][0])
      y3.append(p[i][1][1])
  return(b0,y1,b1,y2,b2,y3)

def normalize(db):
  for i in range(len(db[0,:,0])):
    for c in range(len(db[:,0,0])):
      db[c,i,:]=(db[c,i,:]-np.mean(db[c,i,:]))
  return db

#Params
test=input("n,phi?:")
# stepsTested=int(input("Steps to test:"))
tot=int(input("Total Steps: "))
adin=input("Alpha: ")
# ser=input("State: ")

#Open Data
db=xr.open_dataset(f"/home/jfkiewel/python/3dSpatial/Saved_NC_Files/{adin}_{tot}.nc")
filt_values=normalize(db[test].values[tot,:,:,:])
cc = gd.PeriodicCubicalComplex(top_dimensional_cells = filt_values, periodic_dimensions=[False,True,True])
print("You have been complexed")
cc.compute_persistence()
p=cc.persistence()

#Get the three different persistent holes in 3d Space
b0,y1,b1,y2,b2,y3 =get_betti(p)

def midlife(b,y):
  return (b+y)/2
t1=[]
for i in range(len(b0)):
  if y1[i] != np.inf:
    t1.append(midlife(b0[i],y1[i]))
t2=[]
for i in range(len(b1)):
  if y2[i] != np.inf:
    t2.append(midlife(b1[i],y2[i]))
t3=[]
for i in range(len(b2)):
  if y3[i] != np.inf:
    t3.append(midlife(b2[i],y3[i]))


print("Finished Persistence Calculations")
#Setting Up and Building Figure
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(20, 10))
plt.suptitle(f"Midlife Histograms, alpha={adin}, step={tot}",fontsize=40)

ax1=axes[0,0]
ax1.plot(b0,y1,"gx")
ax1.plot(b1,y2,"rx")
ax1.plot(b2,y3,"bx")

ax2=axes[0,1]
ax2.set_title("Betti 0")
ax2.hist(t1)
ax3=axes[1,0]
ax3.set_title("Betti 1")
ax3.hist(t2)
ax4=axes[1,1]
ax4.set_title("Betti 2")
ax4.hist(t3)
ax2.get_shared_x_axes().join(ax2, ax3)
ax3.get_shared_x_axes().join(ax3, ax4)
ax4.get_shared_x_axes().join(ax4, ax2)
#Saving figure
fig.savefig(f"/home/jfkiewel/python/3dSpatial/plots/{adin}/Midlife_{tot}.png")
plt.close()
print("Job Completed")