# createGrid.py
# Builds the 3D object-based geological grid (channel + 2 lobes) for the
# Nise Formation reservoir model, including Gaussian-random porosity and
# power-law permeability fields. Outputs PORO.INC, PERM.INC, FIPNUM.INC
# for use in the OPM Flow simulation decks in ../simulation/.
#
# Author: Linda Afrifa, MSc Petroleum Geosciences, NTNU (2025)
# Run: pip install numpy matplotlib gstools && python createGrid.py
#
# Original script as used in MSc thesis work, included as-is.

import numpy as np
from random import random
import matplotlib.pyplot as plt
from gstools import SRF, Gaussian


shape=np.array([150,300,50])
dimensions=np.array([30,100,1]) # The physical dimensions of each cell in meters 

propertyModel=np.zeros(shape) #100-meter grid blocks in x and y direction, and 1 meter in z direction, define background as zero


def createOvalLobe(place,radius1,radius2,thickness):
	for xx in range(0,shape[0]):
		for yy in range(0,shape[1]):
			if ((xx-place[0])*dimensions[0])**2/radius1**2+((yy-place[1])*dimensions[1])**2/radius2**2<1:
				for zz in range(place[2],place[2]+thickness):
					propertyModel[xx,yy,zz]=1 #index one indicates a lobe


#def createOneChannel(xposition,depth,width):
	#for xx in range(xposition-width,xposition+width+1):
		#for yy in range(0,shape[1]):
		#for yy in range(0,30):
			#for zz in range(depth,depth+width+1):
				#if np.sqrt((xx-xposition)**2+(zz-depth)**2)<width:
					#propertyModel[xx,yy,zz]=2 #index two indicates a channel




#create the first oval lobe by defining lobe position
place=np.array([75,150,5]) # Center of the lobe (x, y, z)
radius1= 500
radius2= 8000
thickness=3 #3 meters in z-direction as a grid is 1 meter
createOvalLobe(place,radius1,radius2,thickness)


#create the second oval lobe 
# Define position and size for the second lobe, 2 meters below the first lobe
place2 = np.array([place[0], place[1]-3, place[2] + 2])  # New center of the second lobe (x, y, z)
radius1_2 = 600  # Radius in x-direction for the second lobe
radius2_2 = 9000  # Radius in y-direction for the second lobe
thickness_2 = 4  # Thickness of the second lobe in the z-direction
createOvalLobe(place2, radius1_2, radius2_2, thickness_2) # Call the function to create the second lobe

print(f"Second lobe will be placed at: {place2}")  # Debugging output to check coordinates

# Define channel position to extend into the lobe
#xposition = place[0]  # Align x-center of the channel with the lobe
xposition = 75  # Align x-ce
#depth = place[2] # Match the depth of the lobe
depth_start = place[2]  # Channel starts at Z = 5 (first lobe)
depth_end = place2[2] + 2  # Channel ends at Z = 7 (second lobe)
width = 5  # Width of the channel in grid cells
#channel_length_in_lobe = int(30 / dimensions[1])  # Length of channel overlap with lobe in grid cells
channel_length_in_lobe = 30  # Length of channel overlap with the first lobe in Y-direction

def createOneChannel(xposition, yposition_start, depth_start, depth_end, width):
    for zz in range(depth_start, depth_end + 1):
        for xx in range(xposition - width, xposition + width + 1):
            for yy in range(yposition_start, yposition_start + channel_length_in_lobe):
                if np.sqrt((xx - xposition) ** 2 + (yy - yposition_start) ** 2) < width:
                    propertyModel[xx, yy, zz] = 2  # Channel takes precedence


# Now create the channel using the updated depth values
createOneChannel(xposition, place[1], depth_start, depth_end, width)


# Extend the channel to overlap with the lobe
for xx in range(xposition - width, xposition + width + 1):
    for yy in range(0, shape[1]):  # Extend the channel through y-direction
        if yy <= place[1] + channel_length_in_lobe:
            for zz in range(depth_start, depth_end + width + 1): #for zz in range(depth_start, depth_end + 1)
                if np.sqrt((xx - xposition) ** 2 + (zz - depth_start) ** 2) < width:
                    propertyModel[xx, yy, zz] = 2  # Channel takes precedence




#Create a porosity model with petrophysical averages from the 4 well logs 
muBackground = 0.00
muLobes = 0.15
muChannel= 0.20
variance = 0.001

model = Gaussian(dim=3, var=variance, len_scale=int(0.2*shape[0]))
srf = SRF(model, seed=0)
porosityField = srf.structured([range(shape[0]),range(shape[1]),range(shape[2])])
fipnumField = srf.structured([range(shape[0]),range(shape[1]),range(shape[2])])
print(np.shape(porosityField))
porosityField[propertyModel[:]==0]=porosityField[propertyModel[:]==0]*muBackground+muBackground
porosityField[propertyModel==1]=porosityField[propertyModel==1]*muLobes+muLobes
porosityField[propertyModel==2]=porosityField[propertyModel==2]*muChannel+muChannel
porosityField[porosityField<0]=0
fipnumField[:] = 2 # Set the fluid in place number (FIPNUM) for the whole model to 2
fipnumField[propertyModel[:]==0]=1 # Set the fluid in place number (FIPNUM) for the background model to 1


# Update porosity for the second lobe
#porosityField[propertyModel == 1] = porosityField[propertyModel == 1] * muLobes + muLobes

#plt.imshow(porosityField[:,:,int(place[2])], interpolation='nearest')
#plt.show()


multiplicationFactor=9 #you can change the power 8 multiplied to the porosityField to a smaller number to get lower permeabilities in your model
#use the permeability equation from the well log in interactive petrophysics
permField=12**(multiplicationFactor*porosityField-0.1)

#plt.imshow(permField[:,:,int(place[2])], interpolation='nearest')
#plt.show()

#plt.imshow(propertyModel[:,:,10], interpolation='nearest')
#plt.title("Second Lobe Added")
#plt.show()



# Visualize permeability field (both lobes will be the same)
#plt.imshow(permField[:, :, int(place[2])], interpolation='nearest')
#plt.title("Permeability for Lobes")
#plt.show()

# Visualize propertyModel to confirm both lobes are created
#plt.imshow(propertyModel[:, :, int(place[2])], interpolation='nearest')
#plt.title("First and Second Lobe in Property Model")
#plt.show()

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches 

# Visualizing the model with the second lobe included
z_level = place[2]  # Choose a slice that includes both lobes
plt.imshow(propertyModel[:, :, z_level], interpolation='nearest')

# Add title to the plot
plt.title("RESERVOIR REALISATION OF MODEL")

# Create the legend patches based on the existing colors in the plot
background_patch = mpatches.Patch(color='purple', label='Background')  # Assuming background is purple
lobe_patch = mpatches.Patch(color='cyan', label='Lobe')  # Assuming lobes are cyan
channel_patch = mpatches.Patch(color='yellow', label='Channel')  # Assuming channel is yellow


# Add the legend to the plot
plt.legend(handles=[background_patch, lobe_patch, channel_patch], loc='upper right')

# Show the plot with the legend
plt.show()



# Calculate the average porosity and permeability for each feature
avg_porosity_background = np.mean(porosityField[propertyModel == 0])
avg_porosity_lobe = np.mean(porosityField[propertyModel == 1])
avg_porosity_channel = np.mean(porosityField[propertyModel == 2])

avg_perm_background = np.mean(permField[propertyModel == 0])
avg_perm_lobe = np.mean(permField[propertyModel == 1])
avg_perm_channel = np.mean(permField[propertyModel == 2])



poroFile=open('PORO.INC','w')
poroFile.write('PORO \n')
permFile=open('PERM.INC','w')
permFile.write('PERMX \n')
fipnumFile=open('FIPNUM.INC','w')
fipnumFile.write('FIPNUM \n')
for poro in np.ravel(porosityField,order='F'):
	poroFile.write(str(poro)+'\n')
for perm in np.ravel(permField,order='F'):
	permFile.write(str(perm)+'\n')
for fipnum in np.ravel(fipnumField,order='F'):
	fipnumFile.write(str(int(fipnum))+'\n')
poroFile.write('/ \n')
permFile.write('/ \n')
fipnumFile.write('/ \n')

poroFile.close()
permFile.close()
fipnumFile.close()
