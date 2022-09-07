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

def normalize(db):
  for i in range(len(db[0,0,:,0])):
    for c in range(len(db[0,:,0,0])):
      db[0,c,i,:]=(db[0,c,i,:]-np.mean(db[0,c,i,:]))
  return db

#Params
test=input("n,phi,vort?: ")
alpha=input("Alpha: ")
every=int(input("Every _ Steps: "))
ste=int(input("Steps: "))

#Pulling data for last frame (most turblent, best for setting scale)
ds=xr.open_dataset(f"/home/jfkiewel/python/3dSpatial/Saved_NC_Files/{alpha}_{ste}.nc")
db=ds[test].values[::every,:,:,:]
db=normalize(db)
tem=[];x=[]

def met(i):
  filt_values = db[int(i),:,:,:]
  cc = gd.PeriodicCubicalComplex(top_dimensional_cells = filt_values, periodic_dimensions=[False,True,True])
  cc.compute_persistence()
  return len(cc.persistence())

for i in range(1,len(db[:,0,0,0])-1):
  tem.append(met(i))
  x.append((i+1)*every)
  print(f"Finished step {(i+1)*every}")

fig=plt.figure()
plt.xlabel("Steps")
plt.ylabel("Features")
plt.title(f"a={alpha}, NumFeat")
plt.plot(x,tem)
fig.savefig(f"plots/{alpha}/NumFeat_{ste}.png")#plots/{alpha}/
plt.close()