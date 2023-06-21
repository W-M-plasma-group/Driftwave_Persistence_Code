#This code is to add random gaussian noise or pixelation to the persistence diagrams, in order to visualize the changes

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
from time import perf_counter
import random
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
from IPython import display

#Separates persistence list p into betti number classifications
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

#Normalizes out background gradient
def normalize(db):
  for i in range(len(db[0,:,0])):
    for c in range(len(db[:,0,0])):
      db[c,i,:]=(db[c,i,:]-np.mean(db[c,i,:]))
  return db

#Subtracts the diagonals out from persistence data. In this code, this better allows us to analyze structures in comparison to themselves.
def subdiag(b,y):
  sec=[]
  for i in range(len(y)):
    sec.append(y[i]-b[i])
  return sec

#This method adds a gaussian noise up and down for the value of the 
def gaussian(db):
  m=((np.amax(db))*0.05)*1
  for i in range(len(db[0,:,0])):
    for c in range(len(db[:,0,0])):
      for z in range(len(db[0,0,:])):
        db[c,i,z]=db[c,i,z]+random.gauss(db[c,i,z],m)
        print(f"Changed value {db[c,i,z]} to {db[c,i,z]+random.gauss(0,m)} ")
  return db

def pixelation(db,size):
  grid=np.zeros((int(len(db[:,0,0])/size),int(len(db[0,:,0])/size),int(len(db[0,0,:])/size)))
  for i in range(int(len(db[:,0,0])/size)):
    for j in range(int(len(db[0,:,0])/size)):
      for k in range(int(len(db[0,0,:])/size)):
        grid[i][j][k]=sum(np.ravel(db[i*size:i*size+size,j*size:j*size+size,k*size:k*size+size]))/(size**3)
  return regrid(grid,size,db)

def regrid(grid,size,ds):
  # returnable=np.zeros((int(len(db[:,0,0])),int(len(db[0,:,0])),int(len(db[0,0,:]))))
  for i in range(len(ds[:,0,0])):
    for j in range(len(ds[0,:,0])-1):
      for k in range(len(ds[0,0,:])):
        ds[i,j,k]=grid[int(i/size),int(j/size)-1,int(k/size)]
  return ds

#Params
size=1
test=input("n,phi?:")
tot=int(input("Total Steps: "))
adin=input("Alpha: ")
save_name=input("Name of Output plot: ")
noise=input("Pixelation = y/n: ")
if noise =="y":
  size=int(input("Pixel Size (mxm):"))
gaus=input("Gaussian Noise? = y/n: ")

#Open Data from Packager
db=xr.open_dataset(f"raw_data/BOUT.dmp.nc")
ds=db[test].values[tot,2+int((64%size)/2):len(db[test]["x"])-2-(int((64%size)/2)+(64%size)%2),int((16%size)/2):len(db[test]["y"])+int((16%size)/2)+(16%size)%2,int((64%size)/2):len(db[test]["z"])-(int((64%size)/2)+(64%size)%2)]#cuts it into divisible squares
tic=perf_counter()
filt_values=normalize(ds)
toc=perf_counter()
drb=filt_values
if noise == "y":
  drb=pixelation(filt_values,size)
if gaus=="y":
  drb=gaussian(drb)

dap=drb[:,-1,:]

#Setting first frame(which is last frame to set colorbar to reasonable scale)
Figure=plt.figure()
plotte=plt.imshow(dap)
plt.colorbar(plotte)

#Define animationfunction to feed to the FuncAnimation method of matplotlib
def AnimationFuncion(frame):
  dap=drb[:,frame,:]
  plotte.set_array(dap)
  print(frame)
  return plotte

#Animation drawn and saved
anim=FuncAnimation(Figure,AnimationFuncion,frames=len(drb[0,:,0]),interval=200)
FFwriter = animation.FFMpegWriter()
anim.save(f'plots/{adin}/{save_name}_animation.mp4')
plt.close()
