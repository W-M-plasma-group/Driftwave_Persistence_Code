import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt
import xbout as xb
from IPython import display
import xarray as xr
import scipy

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
ds=xr.open_dataset(f"/home/jfkiewel/python/3dSpatial/Saved_NC_Files/{api}_{step}.nc")

db=ds[test].values[:,4:64,0,:]
db=normalize(db)

dap=db[-1,:,:]

#Setting first frame(which is last frame)
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
anim.save(f'plots/{api}/Time_animation.mp4')
plt.close()