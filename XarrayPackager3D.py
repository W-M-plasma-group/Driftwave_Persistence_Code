#The purpose of this code is to take the output files of the BOUT++ simulation framework and save the relevant data into data that can be more easily 
#used for calculations. This includes saving the data with relevant simulation information.
#This has less functionality now since the 3D simulation is too large to do normalization on, and we decided to focus on electron density, and we no longer
#save phi or vort data anyway.


import numpy as np
import netCDF4 as cdf
import xarray as xr
import xbout as xb
import os

#This is some old code that worked for normalization of 2d Frames, and would ensure that the simulation data was normalized before saving the Xarray
#With 3d spatial data, this was too computationally intensive and is done at the level of the code that does computations of the dataset.
#Might no longer work within the code
# def normalize(dn,n):
#   ds=dn[n].values[:,:,0,:]
#   for c in range(nout):
#     for f in range(12,248):
#       rade=ds[c,f,12:244]
#       xar[n].values[c,f-12,:]=rade-np.mean(rade)
#       rade=None
#     print(f"Normalized step {c} of {n}")
#   xar.to_netcdf(f"Saved_NC_Files/{alpha}_{nout}_{region}_temp.nc")
#   os.rename(f"Saved_NC_Files/{alpha}_{nout}_{region}_temp.nc",f"Saved_NC_Files/{alpha}_{nout}_{region}.nc")
#   ds=None


#Honestly, don't know what this older code does. Left it for posterity
# def SetArray(ds,test):
#   db = ds[test].values[-nout:,12:248,0,:]
#   db = normalize(db,test)
#   return xr.DataArray(data=db,dims=['time','x','z'])

#Inputs determine output path and data that will be saved in info array
#These variables were also used to create the path that the output files would be placed in for organizational purposes
nout=int(input("nout: "))
alpha=input("Alpha: ")
kappa=input("Kappa: ")
# region=input("Region: ")

#Retrieve data from from BOUT
ds = xb.open_boutdataset(f"<$BOUT_OUTPUT_PATH.nc>")

#Setting up XArray array object with info, and density data. Previous code also saved vorticity and potential data, but because that data was not used otherwise
#and was storage intensive, decided to just save density data
xar = xr.Dataset({})
xar["info"]=[alpha,kappa,nout]

#Workaround to lazy loading preventing us from updating the XArray that we want to update.
xar["n"]=(["t","x","y","z"],ds["n"].values[:,:,:,:])
xar.to_netcdf(f"<$OUTPUT_PATH>_temp.nc")
os.rename(f"<$OUTPUT_PATH>_temp.nc",f"<$OUTPUT_PATH>.nc")

#Some old code for normalization. The i comes from a loop no longer in the code, I believe.
# normalize(ds,i)
# print(f"Normalize {i} Finished")
xar.close()
ds=None

print("Dataset Complete")
print("Complete")
