import matplotlib.pyplot as plt
import xbout as xb
from xbout import open_boutdataset
import numpy as np
import gudhi as gd
from matplotlib import pyplot
import xarray as xr
import netCDF4 as cdf
import scipy as sp

def rms(db):
	r=np.mean(db**2)
	return np.sqrt(r)

test=input("n,phi,vort?: ")
adin=input("Alpha: ")
tot=input("Steps: ")


ds=xr.open_dataset(f"/home/jfkiewel/python/3dSpatial/Saved_NC_Files/{adin}_{tot}.nc")
db=ds[test].values[:,:,:,:]
ds=0

tem=[];x=[]
for i in range(2,len(db[:,0,0,0])-1):
	tem.append(rms(db[i,:,:,:]))
	x.append(i+2)
	print(f"Timestep {i}")
fig=plt.figure()
plt.xlabel("Steps")
plt.ylabel("RMS")
plt.title(f"RMS")
plt.plot(x,tem)
fig.savefig(f"/home/jfkiewel/python/3dSpatial/plots/{adin}/RMS_3D_{tot}.png")
plt.close()





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
# fig.savefig(f"plots/{alpha}/RMS_{test}.png")
# plt.close()