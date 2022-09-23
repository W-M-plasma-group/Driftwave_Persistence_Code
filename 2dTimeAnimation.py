#This code is part of the transition from 2D to 3D. In order to compare Hasegawa-Wakatani 2D and 3D simulations, wrote this code to look like the output
#of the 2D case, that is to sweep through a time series of the same frame in the 3D space.


import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt
import xbout as xb
from IPython import display
import xarray as xr
import scipy

#Normalizes out the background gradient
def normalize(db):
  for i in range(len(db[:,0,0])):
    for c in range(len(db[0,:,0])):
      db[i,c,:]=(db[i,c,:]-np.mean(db[i,c,:]))
  return db

#Params
test=input("n,phi,vort?: ")
save_name=input("Name of output plot: ")

#Pulling data for last frame (most turblent, best for setting scale)
ds=xr.open_dataset(f"raw_data/BOUT.dmp.nc")

dn=ds[test].values[:,2:len(ds[test]["x"])-2,0,:]
dn=normalize(dn)

f1=dn[-1,:,:]

#Setting first frame(important for colorbar standardization)
Figure=plt.figure()
plotte=plt.imshow(f1)
plt.colorbar(plotte)

#Define animationfunction to feed to the FuncAnimation method of matplotlib
def AnimationFuncion(frame):
  f1=dn[frame,:,:]
  plotte.set_array(f1)
  print(frame)
  return plotte

#Animation drawn and saved. The output video speed is determined by speed of computer- quirk of FuncAnimation
anim=FuncAnimation(Figure,AnimationFuncion,frames=len(dn[:,0,0]),interval=50)
FFwriter = animation.FFMpegWriter()
anim.save(f'plots/{save_name}.mp4')
plt.close()
