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

#Params
test=input("n,phi?:")
stepsTested=int(input("Steps to test:"))
tor=input("Total Steps: ")
tot=int(tor)
adin=input("Alpha: ")
ser=input("State: ")

#Open Data
db=xr.open_dataset(f"/home/jfkiewel/python/Saved_NC_Files/{adin}_{tor}_{ser}.nc")
steps=int(db["info"].values[2])
alpha=db["info"].values[0]
filt_values=db[test].values[steps-stepsTested:steps,:,:]
cc = gd.PeriodicCubicalComplex(top_dimensional_cells = filt_values, periodic_dimensions=[False,False,True])
print("You have been complexed")
cc.compute_persistence()
p=cc.persistence()

#Get the three different persistent holes in 3d Space
b0,y1,b1,y2,b2,y3 =get_betti(p)
# dat1=(np.vstack((b0,y1))).T
# dat2=(np.vstack((b1,y2))).T
# dat3=(np.vstack((b2,y3)))
# db[f"3d_pers_{test}"]=(("Birth","Death"),dat3)
# p=None
# db.to_netcdf(path=f"/home/jfkiewel/python/Saved_NC_Files/{adin}_{tot}_{ser}_temp.nc")
# db.close()

print("Finished Persistence Calculations")
#Setting Up and Building Figure
lims = [min(b0)-0.05,max(b2)+0.05]
fig=plt.figure()
plt.title(f"Persistence of Two Dimensional Data With Time as a Third Dimension, steps={stepsTested}",fontsize=10)
plt.xlabel("Birth",fontsize=20)
plt.ylabel("Death",fontsize=20)
plt.plot(b0,y1,'gx')
plt.plot(b1,y2,'rx')
plt.plot(b2,y3,'bx')
plt.fill_between(lims,lims,y2=lims[0],color='#d3d3d3')

#Saving figure
fig.savefig(f"plots/{adin}/TimePersistencePlot_{test}_{stepsTested}.png")
plt.close()
os.rename(f"/home/jfkiewel/python/Saved_NC_Files/{adin}_{tot}_{ser}_temp.nc",f"/home/jfkiewel/python/Saved_NC_Files/{adin}_{tot}_{ser}.nc")
print("Job Completed")