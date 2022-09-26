#This code is for the calculation of persistence, split the persistence by betti numbers, and then use subplots to give an idea of the overall persistence,
#as well as the persistence of specific betti numbers.
#There is some functionality to store the betti persistences into the Xarray .nc file that all the code uses, but that was more storage intensive for the data
#so far, and calculating persitence again was computationally cheap in comparison.

import matplotlib.pyplot as plt
import xbout as xb
from xbout import open_boutdataset
import numpy as np
import gudhi as gd
from matplotlib import pyplot
import xarray as xr
import netCDF4 as cdf
import scipy as sp
import os
from time import perf_counter

#Separates persistence list p into betti number classifications
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

#Normalizes out background gradient
def normalize(db):
  for i in range(len(db[0,:,0])):
    for c in range(len(db[:,0,0])):
      db[c,i,:]=(db[c,i,:]-np.mean(db[c,i,:]))
  return db

#Subtracts the diagonals out from persistence data. In this code, this better allows us to analyze structures in comparison to themselves.
def subdiag(b,y):
  sec=[]
  for i in range(len(y)):
    sec.append(y[i]-b[i])
  return sec

#Params
test=input("n,phi?:")
tot=int(input("Total Steps: "))
adin=input("Alpha: ")
save_name=input("Name of Output plot: ")

#Open Data from Packager
db=xr.open_dataset(f"raw_data/BOUT.dmp.nc")
ds=db[test].values[tot,2:2:len(ds["test"]["x"])-2,:,:]
tic=time.perf_counter()
filt_values=normalize(ds)
toc=time.perf_counter()
norm=toc-tic
tic=time.perf_counter()
cc = gd.PeriodicCubicalComplex(top_dimensional_cells = filt_values, periodic_dimensions=[False,True,True])
print("You have been complexed")
cc.compute_persistence()
toc=time.perf_counter()
pers=toc-tic
p=cc.persistence()

#Get the three different persistent holes in 3d Space
tic=time.perf_counter()
b0,y1,b1,y2,b2,y3 =get_betti(p)
toc=time.perf_counter()
bet=toc-tic

#This code was to save persistence data to the Xarray. Because this is storage intensive, and doing the calculations repeatedly is 
#not computationally intensive at the scales I was using, this was dropped. 
#Also, this current code does not work, but I can fix it if you contact me about it.
# dat1=(np.vstack((b0,y1))).T
# dat2=(np.vstack((b1,y2))).T
# dat3=(np.vstack((b2,y3))).T
# daye=[dat1,dat2,dat3]
# dat1=dat2=dat3=None
# for e in range(2):
#   xar=xr.DataArray(data={daye[e]},dims=["Birth","Death"])#coords=["B0","B1","B2"]
#   db[f"3d_pers_{test}_b{e}"]=xar
# p=None
# db.to_netcdf(path=f"/home/jfkiewel/python/Saved_NC_Files/{adin}_{tot}_{ser}_temp.nc")
# db.close()
# db=None


print("Finished Persistence Calculations")
#Setting Up and Building Figure/ plots and subplots
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(20, 10))#, sharex=True, sharey=True)
plt.suptitle(f"Diagonals Subtracted out, 3D test",fontsize=30)

ax1=axes[0,0]
ax1.plot(b0,y1,"gx")
ax1.plot(b1,y2,"rx")
ax1.plot(b2,y3,"bx")
ax1.set_xlabel("Birth")
ax1.set_ylabel("Death")
tem=subdiag(b0,y1)
ax2=axes[0,1]
ax2.set_title("Betti 0")
ax2.set_xlabel("Birth")
ax2.set_ylabel("Lifetime")
ax2.plot(b0,tem,"gx")
tem=subdiag(b1,y2)
ax3=axes[1,0]
ax3.set_title("Betti 1")
ax3.set_xlabel("Birth")
ax3.set_ylabel("Lifetime")
ax3.plot(b1,tem,"rx")
tem=subdiag(b2,y3)
ax4=axes[1,1]
ax4.set_title("Betti 2")
ax4.set_xlabel("Birth")
ax4.set_ylabel("Lifetime")
ax4.plot(b2,tem,"bx")
ax2.get_shared_x_axes().join(ax2, ax3)
ax3.get_shared_x_axes().join(ax3, ax4)
ax4.get_shared_x_axes().join(ax4, ax2)

#Saving figure
fig.savefig(f"plots/{save_name}.png")
plt.close()
print("Job Completed") 
print(f"Time for normalization= {norm:0.3f}.\n Time for Persistence Calcuation (From Library)= {pers:0.3f}\n Time for Seperating betti numbers= {bet:0.3f}")
