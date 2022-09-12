#Failed experiment, hoped that I would get a clearer picture that allows for seeing the shape, rather than number of features, which should be possible
#with the right density map, however, I never did, midlife is a better visualization, and I never looked at it again...
#Also, this code works with a stack of 2D in time for 3D data structures.


import matplotlib.pyplot as plt
import xbout as xb
from xbout import open_boutdataset
import numpy as np
import gudhi as gd
from matplotlib import pyplot
import xarray as xr
import netCDF4 as cdf
import seaborn as sns

#Retrieve Betti Numbers
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

#Params
test=input("n,phi,vort?: ")
stepsTested=int(input("Steps to test:"))
ts=int(input("Total Steps: "))
adin=input("Alpha: ")
ser=input("State: ")

#Open Data
db=xr.open_dataset(f"<$SIMULATION_OUTPUT_PATH>.nc")
steps=int(db["info"].values[2])
alpha=db["info"].values[0]
filt_values=db[test].values[steps-stepsTested:steps,:,:]
cc = gd.CubicalComplex(top_dimensional_cells = filt_values)
print("You have been complexed")
cc.compute_persistence()
p=cc.persistence()

#Get the three different persistent holes in 3d Space
b0,y1,b1,y2,b2,y3 =get_betti(p)

print("Finished Persistence Calculations")
#Setting Up and Building Figure
lims = [min(b0)-0.05,max(b2)+0.05]
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(20, 10))
plt.suptitle("Persistence Image of 2 Dimensional Data",fontsize=40)
#Set up Subfig 1
ax1=axes[0,0]
ax1.set_xlabel("Birth",fontsize=20)
ax1.set_ylabel("Death",fontsize=20)
ax1.plot(b0,y1,'gx')
ax1.plot(b1,y2,'rx')
ax1.plot(b2,y3,'bx')
ax1.fill_between(lims,lims,y2=lims[0],color='#d3d3d3')


ax2=axes[0,1]
ax2.set_title("Betti 0")
sns.kdeplot(ax=ax2, x = b0, y = y1, shade = True, cmap = "PuBu")#, bw_method = .5)
ax3=axes[1,0]
ax3.set_title("Betti 1")
sns.kdeplot(ax=ax3,x = b1, y = y2, shade = True, cmap = "PuBu")#, bw_method = .5)
ax4=axes[1,1]
ax4.set_title("Betti 2")
sns.kdeplot(ax=ax4,x = b2, y = y3, shade = True, cmap = "PuBu", bw_method =.1)


# plt.title(f"Persistence of Two Dimensional Data With Time as a Third Dimension, steps={stepsTested}",fontsize=10)
# plt.xlabel("Birth",fontsize=20)
# plt.ylabel("Death",fontsize=20)
# plt.plot(b0,y1,'gx')
# plt.plot(b1,y2,'rx')
# plt.plot(b2,y3,'bx')
# plt.fill_between(lims,lims,y2=lims[0],color='#d3d3d3')

#Saving figure
fig.savefig(f"<$OUTPUT_PLOT>.png")
plt.close()
print("Job Completed")
