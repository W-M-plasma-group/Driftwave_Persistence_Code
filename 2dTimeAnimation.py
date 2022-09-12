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
api=input("Alpha: ")
step=int(input("Steps: "))
# reg=input("Region: ")

#Pulling data for last frame (most turblent, best for setting scale)
ds=xr.open_dataset(f"<$SIMULATION_OUTPUT_PATH>.nc")

db=ds[test].values[:,4:64,0,:]
db=normalize(db)

dap=db[-1,:,:]

#Setting first frame(important for colorbar standardization)
Figure=plt.figure()
plotte=plt.imshow(dap)
plt.colorbar(plotte)

#Define animationfunction to feed to the FuncAnimation method of matplotlib
def AnimationFuncion(frame):
  dap=db[frame,:,:]
  plotte.set_array(dap)
  print(frame)
  return plotte

#Animation drawn and saved
anim=FuncAnimation(Figure,AnimationFuncion,frames=len(db[:,0,0]),interval=50)
FFwriter = animation.FFMpegWriter()
anim.save(f'<$OUTPUT_PATH>.mp4')
plt.close()
