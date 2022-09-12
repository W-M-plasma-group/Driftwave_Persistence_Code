import matplotlib.pyplot as plt
import xbout as xb
from xbout import open_boutdataset
import numpy as np
import gudhi as gd
import pandas as pd
from matplotlib import pyplot
import xarray as xr
import os

def plotter(s): 
  filt_values=dn[s,:,:]
  cc = gd.CubicalComplex(top_dimensional_cells = filt_values)
  cc.compute_persistence()
  p=cc.persistence()
  b0=[];y1=[];b1=[];y2=[] #Retrieving Betti number persistences
  for i in range(len(p)):
    if p[i][0]==0:
      b0.append(p[i][1][0])
      y1.append(p[i][1][1])
    elif p[i][0]==1:
      b1.append(p[i][1][0])
      y2.append(p[i][1][1])
  if b1!= []:
    lims = [min(b0)-0.05,max(b1)+0.05]
  else:
    lims = [min(b0)-0.05,max(b0)+0.1]

#Set up figure
  fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))
  plt.suptitle("Persistence Image of 2 Dimensional Data",fontsize=40)

#Set up Subfig 1
  ax1=axes[0]
  ax1.set_xlabel("Birth",fontsize=20)
  ax1.set_ylabel("Death",fontsize=20)
  ax1.plot(b0,y1,'gx')
  ax1.plot(b1,y2,'rx')
  ax1.fill_between(lims,lims,y2=lims[0],color='#d3d3d3')

#Set up Subfig 2
  ax2=axes[1]
  ax2.imshow(filt_values)

#Save Figures
  fig.savefig(f"plots/{alpha}/PersistencePlot{l}_{test}_.png")
  plt.close()

#Retrieving Data
alpha=input("Alpha: ")
fir=input("Phase State: ")
ste=input("Steps: ")
ds=xr.open_dataset(f"/home/jfkiewel/python/Saved_NC_Files/{alpha}_{ste}_{fir}.nc")
test=input("Value Type (n,phi,vort): ")
dn=ds[test].values[:,:,:]
steps=len(dn[:,0,0])

#Loop to get a bunch of plots at different times for same simulation
for l in range(1,10):
  s=l*int(steps/10)
  plotter(s)
  print(f"Saved Plot {l}")