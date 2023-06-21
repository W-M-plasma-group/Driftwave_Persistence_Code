import numpy as np
import xarray as xr
from PIL import Image, ImageFilter
import random
import scipy as sp
import scipy.ndimage
import gudhi as gd
import gudhi.wasserstein as gdwas
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation

#Only used for testing purposes. Write your own code to pull things
def openthedata():
  test=input("Simulation Info Desired (n, phi, vort): ")
  data=xr.open_dataset(f"Simulation/BOUT.dmp.0.nc")#/home/jfkiewel/python/2023/
  #info=data["info"].values
  data=data[test].values[len(data[test]["t"])-1,2:len(data[test]["x"])-2,0,:]
  return data

#This method pixelates data with size representing how each larger pixel is the mean of a size x size group of pixels in original
#The output needs work, specifically for the case that the image cannot cleanly be divided by size.
def pixelate(tempdata,size):
  if len(tempdata[:,0])%size!=0:
    tempdata=tempdata[int((len(tempdata[:,0])%size)/2):len(tempdata[:,0])-(int((len(tempdata[:,0])%size)/2)+(len(tempdata[:,0])%size)%2),:]
  if len(tempdata[0,:])%size!=0:
    tempdata=tempdata[:,int((len(tempdata[0,:])%size)/2):len(tempdata[0,:])-(int((len(tempdata[0,:])%size)/2)+(len(tempdata[0,:])%size)%2)]
  grid=np.zeros((int(len(tempdata[:,0])/size),int(len(tempdata[0,:])/size)))
  for i in range(int(len(tempdata[:,0])/size)):
    for j in range(int(len(tempdata[0,:])/size)):
      grid[i][j]=sum(np.ravel(tempdata[i*size:i*size+size,j*size:j*size+size]))/(size**2)
  returnable=np.zeros((int(len(tempdata[:,0])),int(len(tempdata[0,:]))))
  for i in range(int(len(tempdata[:,0]))):
    for j in range(int(len(tempdata[0,:]))):
      returnable[i][j]=grid[int(i/size)][int(j/size)]
  #print(f"Pixelation Complete {size}x{size}")
  return returnable

#Adds gaussian noise to the image data fed in. This is from the random package, with mean equal to pixel value, and sigma being proportional to the max of the data
def noisegauss(tempdata,sigmamod):
  returnable=np.zeros((int(len(tempdata[:,0])),int(len(tempdata[0,:]))))
  m=((np.amax(tempdata))*0.05)*sigmamod
  for i in range(int(len(tempdata[:,0]))):
    for j in range(int(len(tempdata[0,:]))):
      returnable[i][j]=tempdata[i,j]+random.gauss(tempdata[i,j],m)
  #print(f"Gaussian Noise Added, sigma={m}")
  return returnable

#Random Poisson noise added from python random package
def noisepoisson(tempdata):
  # returnable=np.zeros((int(len(tempdata[:,0])),int(len(tempdata[0,:]))))
  returnable=np.random.poisson(tempdata)
  # for i in range(int(len(tempdata[:,0]))):
  #   for j in range(int(len(tempdata[0,:]))):
  #     returnable[i][j]=noised[i][j]
  return returnable  

#Future salt and peper noise
def noiseSP():
  return

#The driving of turbulence in our Hasegawa-Wakatani physics simulations is through a background gradient. This normalizes that background out.
#It works by taking the average of each row and subtracting it out, rather than removing the actual background gradient. This means that some major turbulence can cause individual rows to be a little rough
#Should have no problem for persistence diagrams for the most part
def normalize(tempdata):
  returnable=np.zeros((int(len(tempdata[:,0])),int(len(tempdata[0,:]))))
  for i in range(len(tempdata[:,0])):
    returnable[i]=tempdata[i,:]-np.mean(tempdata[i,:])
  return returnable

#3D array is visualized throuh mp4 video sweeping though 1st dimension. Colorbar is normalized to last frame to deal with time series
def visualize(viddata):
  def AnimationFuncion(frame):
    dap=viddata[frame]
    plotte.set_array(dap)
    #print(frame)
    return plotte
  dap=viddata[-1]
  #Setting first frame(which is last frame to set colorbar to reasonable scale)
  Figure=plt.figure()
  plotte=plt.imshow(dap)
  plt.colorbar(plotte)
  #Animation drawn and saved
  anim=FuncAnimation(Figure,AnimationFuncion,frames=len(viddata),interval=200)
  FFwriter = animation.FFMpegWriter()
  output_path=input("Save animation with name: ")
  anim.save(f'{output_path}.mp4')
  plt.close()

#Wasserstein comparison of two different image arrays
def wasserbetti(temppersistence):
  b=[];y=[]
  for i in range(len(temppersistence)):
    b.append(temppersistence[i][1][0])
    y.append(temppersistence[i][1][1])
  return np.vstack((b,y)).T
def WassersteinCompare(img1,img2):
  ccimg1=gd.PeriodicCubicalComplex(top_dimensional_cells=img1,periodic_dimensions=[False,True]);ccimg2=gd.PeriodicCubicalComplex(top_dimensional_cells=img2,periodic_dimensions=[False,True])
  ccimg1.compute_persistence();ccimg2.compute_persistence()
  pimg1=ccimg1.persistence();pimg2=ccimg2.persistence()
  cimg1=wasserbetti(pimg1);cimg2=wasserbetti(pimg2)
  return gdwas.wasserstein_distance(cimg2,cimg1,order=1.,internal_p=2.)

def get_betti_pers(p):
  b0=[];y1=[];b1=[];y2=[];b2=[];y3=[]
  for i in range(len(p)):
    if p[i][0]==0:
      b0.append(p[i][1][0])
      y1.append(p[i][1][1])
    elif p[i][0]==1:
      b1.append(p[i][1][0])
      y2.append(p[i][1][1])
  return(b0,y1,b1,y2)
def persinfo(tempdata):#I need to check if we can have betti 2 etc in this, and check if I need to keep that
  cc = gd.PeriodicCubicalComplex(top_dimensional_cells = tempdata, periodic_dimensions=[False,True])
  cc.compute_persistence()
  p=cc.persistence()
  b0,y1,b1,y2 =get_betti_pers(p)
  lims = [np.amin(b0)-0.05,np.amax(b1)+0.05]
  fig=plt.figure()
  plt.xlabel("Birth",fontsize=20)
  plt.ylabel("Death",fontsize=20)
  plt.plot(b0,y1,'gx',label="Betti 0 Features")
  plt.plot(b1,y2,'rx',label="Betti 1 Features")
  plt.legend()
  plt.fill_between(lims,lims,y2=lims[0],color='#d3d3d3')
  return fig

#Converts image from pixel data to greyscale image object. Maybe this is a bad idea though? It is. Looking for alternatives
def convertimg(tempdata):
  tempdata=tempdata+abs(np.amin(tempdata))
  tempmax=np.amax(tempdata)
  for i in range(len(tempdata)):
    for j in range(len(tempdata[0])):
      tempdata[i][j]=int((tempdata[i][j]/tempmax)*255)
  tempdata=tempdata.astype(np.uint8)
  temp_image=Image.fromarray(tempdata)
  temp_image.convert("L")
  #print("Return type is now Image")
  return temp_image

#Deprecated PIL blurs
# def gaussblur(tempdata,rad):
#   tempdata=convertimg(tempdata)
#   returnable=tempdata.filter(ImageFilter.GaussianBlur(radius=rad))
#   return np.array(returnable)

# def medianblur2(tempdata,kern):
#   tempdata=convertimg(tempdata)
#   returnable=tempdata.filter(ImageFilter.MedianFilter(size=kern))
#   return np.array(returnable)

def modeblur(tempdata,kern):
  tempdata=convertimg(tempdata)
  returnable=tempdata.filter(ImageFilter.ModeFilter(size=kern))
  return np.array(returnable)

def gaussblur(tempdata,sigma):
  return sp.ndimage.gaussian_filter(tempdata,sigma)

def medianblur(tempdata,kern):
  return sp.ndimage.median_filter(tempdata,size=kern)

# def normalize(db):
#   for i in range(len(db[0,:,0])):
#     for c in range(len(db[:,0,0])):
#       db[c,i,:]=(db[c,i,:]-np.mean(db[c,i,:]))
#   return db

