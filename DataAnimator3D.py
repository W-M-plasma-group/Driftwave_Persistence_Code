#This is too many imports, but I don't know which ones exactly are used by AnimationFunction, so I will just leave as is.
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt
import xbout as xb
from IPython import display
import xarray as xr
import scipy

#Method normalizes out the density gradient
def normalize(db):
  for i in range(len(db[0,:,0])):
    for c in range(len(db[:,0,0])):
      db[c,i,:]=(db[c,i,:]-np.mean(db[c,i,:]))
  return db

#Input params
test=input("n,phi,vort?: ")
api=input("Alpha: ")
step=int(input("Steps: "))
# reg=input("Region: ")

#Pulling data from our saved .nc file (Xarray)
ds=xr.open_dataset(f"/home/jfkiewel/python/3dSpatial/Saved_NC_Files/{api}_{step}.nc")

db=ds[test].values[step,4:64,:,:]
db=normalize(db)

dap=db[:,-1,:]

#Setting first frame(which is last frame to set colorbar to reasonable scale)
Figure=plt.figure()
plotte=plt.imshow(dap)
plt.colorbar(plotte)

#Define animationfunction to feed to the FuncAnimation method of matplotlib
def AnimationFuncion(frame):
  dap=db[:,frame,:]
  plotte.set_array(dap)
  print(frame)
  return plotte

#Animation drawn and saved
anim=FuncAnimation(Figure,AnimationFuncion,frames=len(db[0,:,0]),interval=200)
FFwriter = animation.FFMpegWriter()
anim.save(f'plots/{api}/animation.mp4')
plt.close()