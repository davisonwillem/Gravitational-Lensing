import numpy as np 
import matplotlib.pyplot as plt
from PIL import Image

#%%# define constants

sig=1500
Rc=0.07
Ds=878
Dl=637
Dls=442
c=3e5
thetaE=4*np.pi*sig**2*Dls/(Ds*c**2)
rc=Rc/(Dl*thetaE)

#%%# point source production

def genpointsource(r:int):
    # sources and images are defined as rxr arrays of brightnesses, later converted into plots
    source=np.zeros((r,r))
    # if the pixels size is even, make a square point source
    if r%2==0:
        mid=round(r/2)
        source[mid,mid]=1
        source[mid-1,mid]=1
        source[mid,mid-1]=1
        source[mid-1,mid-1]=1
    # if it is odd, a single central pixel
    else:
        mid=round(r/2-0.5)
        source[mid,mid]=1
    return(source)

#%%# chess board source production

def chessboard(r:int):
    # defining an array of 0s and 2s to make a chess board
    source=np.zeros((r,r))
    for i in range (r):
        for j in range (r):
            if (i+j)%2==0:
                source[i,j]=2
    return source

#%%# source generation function

def gensource(r:int,n:int):
    source=np.zeros((r,r))
    # loop through galaxys
    for i in range(n):
        # random position for each galaxy
        galcentx=np.random.randint(r)
        galcenty=np.random.randint(r)
        # random brightness / ellipticity
        a=np.random.randint(r/5,r)/r
        b=np.random.randint(r/5,r)/r
        peakbright=0.25/(a**2+b**2)
        # loop through all pixels
        for j in range(r):
            for k in range(r):
                # if statements to make sure the selected pixel is in range of the array
                if galcentx+j<r and galcenty+k<r:
                    # add the current brightness of the pixel to the brightness from the current galaxy
                    source[galcentx+j,galcenty+k]=source[galcentx+j,galcenty+k]+peakbright/((a*j)**2+(b*k)**2+1)
                if -1<galcentx-j and -1<galcenty-k:
                    source[galcentx-j,galcenty-k]=source[galcentx-j,galcenty-k]+peakbright/((a*j)**2+(b*k)**2+1)
                if -1<galcentx-j and galcenty+k<r:
                    source[galcentx-j,galcenty+k]=source[galcentx-j,galcenty+k]+peakbright/((a*j)**2+(b*k)**2+1)
                if -1<galcenty-k and galcentx+j<r:
                    source[galcentx+j,galcenty-k]=source[galcentx+j,galcenty-k]+peakbright/((a*j)**2+(b*k)**2+1)
    return(source)

#%%# image generation function

def genimage(r:int,source:np.array,eps):
    image=np.zeros((r,r))
    # loop through all pixels in reduced coordinates
    for i in np.linspace(-1+1/r,1-1/r,r):
        for j in np.linspace(-1+1/r,1-1/r,r):
            # define lensed coordinate position
            a=i-i*(1-eps)/(rc**2+(1-eps)*i**2+(1+eps)*j**2)**0.5
            b=j-j*(1+eps)/(rc**2+(1-eps)*i**2+(1+eps)*j**2)**0.5
            # equate image to source brightness, simultaneously converting back to pixel coords
            image[int(round(0.5*(r-1)*(i/(1-1/r)+1))),int(round(0.5*(r-1)*(j/(1-1/r)+1)))]=source[int(round(0.5*(r-1)*(a/(1-1/r)+1))),int(round(0.5*(r-1)*(b/(1-1/r)+1)))]
    return image       

#%%# source plotting function

def sourceplot(r,source:np.array):
    plt.figure(figsize=(10,10))
    plt.axis([0,r,r,0])
    plt.xlabel("$x$ pixels",fontsize=16)
    plt.ylabel("$y$ pixels",fontsize=16)
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    # loop through pixels
    for i in range(r):
        for j in range(r):
            # make all pixles black
            plt.gca().add_patch(plt.Rectangle((i,j),1,1,linewidth=10/r,ec="white",fc="black"))
            brightness=source[i,j]
            # make different pixels different colours depending of brightness
            if 0<brightness<1:
                plt.gca().add_patch(plt.Rectangle((i,j),1,1,linewidth=10/r,ec="white",fc="blue",alpha=brightness))
            elif brightness>=1:
                plt.gca().add_patch(plt.Rectangle((i,j),1,1,linewidth=10/r,ec="white",fc="blue"))
                if brightness>2:
                    plt.gca().add_patch(plt.Rectangle((i,j),1,1,linewidth=10/r,ec="white",fc="white",alpha=1))
                else:
                    plt.gca().add_patch(plt.Rectangle((i,j),1,1,linewidth=10/r,ec="white",fc="white",alpha=brightness-1))
    plt.show()

#%%# image plotting function

def imageplot(r,source:np.array,image:np.array):
    plt.figure(figsize=(10,10))
    plt.axis([0,r,r,0])
    plt.xlabel("$x$ pixels",fontsize=16)
    plt.ylabel("$y$ pixels",fontsize=16)
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    # loop through pixels
    for i in range(r):
        for j in range(r):
            # make all pixles black
            plt.gca().add_patch(plt.Rectangle((i,j),1,1,linewidth=10/r,ec="white",fc="black"))
            brightness=image[i,j]
            # make different pixels different colours depending of brightness
            if 0<brightness<1:
                plt.gca().add_patch(plt.Rectangle((i,j),1,1,linewidth=10/r,ec="white",fc="blue",alpha=brightness))
            elif brightness>=1:
                plt.gca().add_patch(plt.Rectangle((i,j),1,1,linewidth=10/r,ec="white",fc="blue"))
                if brightness>2:
                    plt.gca().add_patch(plt.Rectangle((i,j),1,1,linewidth=10/r,ec="white",fc="white",alpha=1))
                else:
                    plt.gca().add_patch(plt.Rectangle((i,j),1,1,linewidth=10/r,ec="white",fc="white",alpha=brightness-1))
    plt.show()
    
#%%# different ways of producing plots

def pointplot():
    # user inputs
    r=int(input("\nPixels (nxn): "))
    eps=float(input("Value of eps: "))
    # call on correct functions to produce point plot and image generation
    source=genpointsource(r)
    sourceplot(r,source)
    image=genimage(r,source,eps)
    imageplot(r,source,image)
    
def standardplot():
    r=int(input("\nPixels (nxn): "))
    n=int(input("How man galaxys: "))
    eps=float(input("Value of eps: "))
    source=gensource(r,n)
    sourceplot(r,source)
    image=genimage(r,source,eps)
    imageplot(r,source,image)
    
def chessplot():
    r=int(input("\nPixels (nxn): "))
    eps=float(input("Value of eps: "))
    source=chessboard(r)
    sourceplot(r,source)
    image=genimage(r,source,eps)
    imageplot(r,source,image)

def uploadedim(im,eps):
    # convert image into an rxrx3 array
    pixels=np.array(im)
    r=pixels[:,0,0].size
    # break array into 3 rxr array for brightnesses of each rgb colour
    rs=pixels[:,:,0]/255
    gs=pixels[:,:,1]/255
    bs=pixels[:,:,2]/255
    # lense each colour array
    rst=genimage(r,rs,eps)
    gst=genimage(r,gs,eps)
    bst=genimage(r,bs,eps)
    plt.figure(figsize=(10,10))
    plt.axis([0,r,r,0])
    plt.xlabel("$x$ pixels",fontsize=16)
    plt.ylabel("$y$ pixels",fontsize=16)
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    # recombine array into rxrx3
    pstitch=np.stack([rst,gst,bst],axis=2)
    # show lensed image
    plt.imshow(pstitch)
    plt.show()
    
def varyingeps(im):
    slides=int(input("\nNumber of frames: "))
    minmax=float(input("Upper and lower limits of ellipticity, i.e. -a -> +a : "))
    # loop through image generation with different eps values
    for eps in np.linspace(-minmax,minmax,slides):
        uploadedim(im,eps)
    
def movupim(im):
    pixels=np.array(im)
    r=pixels[:,0,0].size
    rs=pixels[:,:,0]/255
    gs=pixels[:,:,1]/255
    bs=pixels[:,:,2]/255
    slides=int(input("\nNumber of frames: "))
    eps=float(input("Value of eps: "))
    # iterate through number of slides
    for k in range(slides):
        rst=np.zeros([r,r])
        gst=np.zeros([r,r])
        bst=np.zeros([r,r])
        # loop through each pixel in reduced coordinates
        for i in np.linspace(-1+1/r,1-1/r,r):
            for j in np.linspace(-1+1/r,1-1/r,r):
                a=i-i*(1-eps)/(rc**2+(1-eps)*i**2+(1+eps)*j**2)**0.5
                b=j-j*(1+eps)/(rc**2+(1-eps)*i**2+(1+eps)*j**2)**0.5
                # lensing must be redefined to work through each square slide of the image
                rst[int(round(0.5*(r-1)*(i/(1-1/r)+1))),int(round(0.5*(r-1)*(j/(1-1/r)+1)))]=rs[int(round(0.5*(r-1)*(a/(1-1/r)+1))),int(round(0.5*(r-1)*(b/(1-1/r)+1))+k*(pixels[0,:,0].size-r)/slides)]
                gst[int(round(0.5*(r-1)*(i/(1-1/r)+1))),int(round(0.5*(r-1)*(j/(1-1/r)+1)))]=gs[int(round(0.5*(r-1)*(a/(1-1/r)+1))),int(round(0.5*(r-1)*(b/(1-1/r)+1))+k*(pixels[0,:,0].size-r)/slides)]
                bst[int(round(0.5*(r-1)*(i/(1-1/r)+1))),int(round(0.5*(r-1)*(j/(1-1/r)+1)))]=bs[int(round(0.5*(r-1)*(a/(1-1/r)+1))),int(round(0.5*(r-1)*(b/(1-1/r)+1))+k*(pixels[0,:,0].size-r)/slides)]
        plt.figure(figsize=(10,10))
        plt.axis([0,r,r,0])
        plt.xlabel("$x$ pixels",fontsize=16)
        plt.ylabel("$y$ pixels",fontsize=16)
        plt.xticks(fontsize=13)
        plt.yticks(fontsize=13)
        pstitch=np.stack([rst,gst,bst],axis=2)
        plt.imshow(pstitch)
        plt.show()

#%%# interface for selecting function and parameters

print("\n\nCurrently, rc is set to ",rc)
rcchange=input("If you would like to change this, input 'y', anything else for no: \n")
if rcchange=="y":
    rc=float(input("Please give a new value of rc: \n"))
p=0
# loop until user inputs stop program
while p==0:
    print("\n1 - Point Plot\n2 - Random Galaxy Distribution Plot\n3 - Chess Plot\n4 - Lens Uploaded Image\n5 - Varying Ellipticity of Uploaded Image\n6 - Moving Lens of Uploaded Image\n0 - Recommended Values for Each Functoin\n10 - Stop Program\n")
    choice=int(input("Please select from the above options which function to run: \n"))
    if choice==0:
        print("\n\nPoint Plot;\n\n   Pixels:                  11 \u2192 101\n   Ellipticity:             -0.1 \u2192 0.1\n")
        print("Random Galaxy Distribution Plot;\n\n   Pixels:                  11 \u2192 101\n   Number of Galaxys:       \u22480.5*Pixels\n   Ellipticity:             -0.3 \u2192 0.3\n")
        print("Chess Plot;\n\n   Pixels:                  11 \u2192 101\n   Ellipticity:             -0.3 \u2192 0.3\n")
        print("Lens Uploaded Image;\n\n   Ellipticity:             -0.3 \u2192 0.3\n")
        print("Varying Ellipticity of Uploaded Image;\n\n   Frames:                  5 \u2192 100\n   Ellipticity Limits:      0.1 \u2192 0.6\n")
        print("Moving Lens of Uploaded Image;\n\n   Frames:                  5 \u2192 100\n   Ellipticity:             -0.3 \u2192 0.3\n\n")
    elif choice==1:
        pointplot()
    elif choice==2:
        standardplot()
    elif choice==3:
        chessplot()
    elif choice==4:
        im=Image.open('starssquare.png')
        eps=float(input("\nValue of eps: "))
        plt.figure(figsize=(10,10))
        plt.xlabel("$x$ pixels",fontsize=16)
        plt.ylabel("$y$ pixels",fontsize=16)
        plt.xticks(fontsize=13)
        plt.yticks(fontsize=13)
        plt.imshow(im)
        uploadedim(im,eps)
    elif choice==5:
        im=Image.open('starssquare.png')
        varyingeps(im)
    elif choice==6:
        im=Image.open('stars.jpg')
        movupim(im)
    elif choice==10:
        p=1
    else:
        print("\n\n---------------\nIncorrect Input\n---------------\n\n")