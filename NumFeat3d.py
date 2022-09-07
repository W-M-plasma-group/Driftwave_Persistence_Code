#The purpose of this code is to plot the number of features over time. This data served originally as a sort of stability indicator.
#Turns out to be a pretty poor indicator, but the code still has a use, as the number of features is important because number of features
#can sometimes be an important indicator of phase change, or could also obfuscate the structures we really want to see.

import matplotlib.pyplot as plt
import numpy as np
import gudhi as gd
from matplotlib import pyplot
import xarray as xr
import os

#Normalization removes the magnetic gradient from the data
def normalize(db):
  for i in range(len(db[0,0,:,0])):
    for c in range(len(db[0,:,0,0])):
      db[0,c,i,:]=(db[0,c,i,:]-np.mean(db[0,c,i,:]))
  return db

#Params for pulling data from path
#The option for every x steps is because this calculation can take a long time for every
test=input("n,phi,vort?: ")
alpha=input("Alpha: ")
every=int(input("Every _ Steps: "))
ste=int(input("Steps: "))

#Pulling data for last frame (most turblent, best for setting scale)
ds=xr.open_dataset(f"<$Saved_Data_Path>.nc")
db=ds[test].values[::every,:,:,:]
db=normalize(db)
tem=[];x=[]

#Method takes each individual timestep for the data and returns the number of features in that timestep
def met(i):
  filt_values = db[int(i),:,:,:]
  cc = gd.PeriodicCubicalComplex(top_dimensional_cells = filt_values, periodic_dimensions=[False,True,True])
  cc.compute_persistence()
  return len(cc.persistence())

#Parsing through timesteps and adding data to array in order to plot 
for i in range(1,len(db[:,0,0,0])-1):
  tem.append(met(i))
  x.append((i+1)*every)
  print(f"Finished step {(i+1)*every}")

#Code saves number of features into same Xarray as the data is stored. This is for future use in dividing out the number of features
#to get a better view of the studied structures, rather than number of features being the largest indication of different persistence
#Will update if this is actually ever used in future
xar["feat"]=(["t","f"],[x,tem])
xar.to_netcdf(f"<$OUTPUT_PATH>_temp.nc")
os.rename(f"<$OUTPUT_PATH>_temp.nc",f"<$OUTPUT_PATH>.nc")

#Setting up figure
fig=plt.figure()
plt.xlabel("Steps")
plt.ylabel("Features")
plt.title(f"a={alpha}, NumFeat")
plt.plot(x,tem)
fig.savefig(f"<$OUTPUT_PATH>.png")
plt.close()
