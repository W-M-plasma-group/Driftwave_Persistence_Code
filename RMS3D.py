#This code is here in order to have a better idea of the stability of the features we are observing by creating a visual of the RMS as a function of simulation timesteps.
#If the RMS has unstable end behavior, then the simulation needs to run for more timesteps, or if there is a periodic nature to the RMS, then the final data should be taken from frames accross
#multiple peaks.

import matplotlib.pyplot as plt
import numpy as np
import gudhi as gd
from matplotlib import pyplot
import xarray as xr

#Method to calculate rms of 3D step (data structure passed is 3D array)
def rms(db):
	r=np.mean(db**2)
	return np.sqrt(r)

#Inputs determine the path to find the Xarray in xr.open_dataset below
test=input("n,phi,vort?: ")
adin=input("Alpha: ")
tot=input("Steps: ")


ds=xr.open_dataset(f"<$Simulation_Data_Xarray>.nc")
db=ds[test].values[:,:,:,:]
ds=0

tem=[];x=[]
for i in range(2,len(db[:,0,0,0])-1):
	tem.append(rms(db[i,:,:,:]))
	x.append(i+2)
	print(f"Timestep {i}")

#Setting up Figure for RMS as a function of timesteps
fig=plt.figure()
plt.xlabel("Steps")
plt.ylabel("RMS")
plt.title(f"RMS")
plt.plot(x,tem)
fig.savefig(f"<$OUTPUT_PATH>.png")
plt.close()




#Some old broken code, did not remove, but should be obsolete.
# plotte=[];x=[]
# for i in range(2,len(db[:,0,0])-1):
# 	tem=[]
# 	for c in range(len(db[0,:,0])):
# 		dv=(db[i,c,:])**2
# 		tem.append(np.mean(dv))
# 	plotte.append(np.mean(tem))
# 	x.append(i+1)
# np.sqrt(plotte)
# fig=plt.figure()
# plt.xlabel("Steps")
# plt.ylabel("RMS")
# plt.title(f"a={alpha}, RMS")
# plt.plot(x,plotte)
# fig.savefig(f"<>")
# plt.close()
