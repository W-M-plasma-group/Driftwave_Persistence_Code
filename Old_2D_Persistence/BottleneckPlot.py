#Old stability measurement. Considered worse than, and far more compuationally expensive than the RMS calculations we see later.

import matplotlib.pyplot as plt
import xbout as xb
from xbout import open_boutdataset
import numpy as np
import gudhi as gd
from matplotlib import pyplot
import xarray as xr

#Params
test=input('n,phi,vort?') #WhichTest
adi=input("alpha: ")
ste=input("Steps: ")
reg=input("Region: ")
plotte=[];x=[]
db= xr.open_dataset(f"<$SIULATION_OUTPUT_DATA>.nc")
steps=int(db['info'].values[2])
alpha=db['info'].values[0]

def pers(step):
	filt_values=db[test].values[step,:,:]
	cc = gd.CubicalComplex(top_dimensional_cells = filt_values)	
	cc.compute_persistence()
	p=cc.persistence()
	b=[];y=[] #Retrieving Betti number persistences
	for i in range(len(p)):
		b.append(p[i][1][0])
		y.append(p[i][1][1])	
	return np.vstack((b,y)).T

step=1
c1=pers(step)

for l in range(5,steps):
	step=l
	c2=pers(step)
	imp=gd.bottleneck_distance(c1,c2,0.005)
	plotte.append(imp)
	x.append(l)
	print(f"Step {l}, {imp}")
	c1=c2
	
fig=plt.figure()
plt.plot(x,plotte)
fig.savefig(f"<$OUTPUT_PLOTS>.png")
plt.close()
