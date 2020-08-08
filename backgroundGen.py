import sys
import os
import ntpath
import shutil
from zipfile import ZipFile 
from PIL import Image, ImageDraw

# possible files for multi direction zip
# directions will be assigned a binary number based on:
# 1111 = urld 
# meaning something that has up, right and downwould be 1101 or 13
# 0  - 0b0000 - isl - island, no connections
# 1  - 0b0001 - do  - down only 
# 2  - 0b0010 - lo  - left only 
# 3  - 0b0011 - ld  - left and down 
# 4  - 0b0100 - ro  - right only
# 5  - 0b0101 - rd  - right and down
# 6  - 0b0110 - rl  - right and left
# 7  - 0b0111 - rld - right, left, and down 
# 8  - 0b1000 - uo  - up only 
# 9  - 0b1001 - ud  - up and down
# 10 - 0b1010 - ul  - up and left 
# 11 - 0b1011 - uld - up, left, and down
# 12 - 0b1100 - ur  - up and right 
# 13 - 0b1101 - urd - up, right, and down
# 14 - 0b1110 - url - up, right, and left
# 15 - 0b1111 - all - all directions 

def makeImg(width, height, binaryfile, imageName):
    with open(binaryfile, 'r') as file:
        binStr = file.read().replace('\n', '')

    im = Image.open(imageName) 
    print("Creating image height:", height, "width", width, "using image", imageName)
    if (im.size[0] != im.size[1]):
        print("image not square")
        quit()

    denom = im.size[0]
    if (width%denom != 0 or height%denom != 0):
        print("size of image does not evenly go into width or height")
        quit()
        
    while (len(binStr) < int((width/denom)*(height/denom))):
        binStr += binStr

    img = Image.new('RGB', (width, height), color = 'white')
    img.putalpha(0)

    x = 0
    y = 0
    for y in range(0,height,denom):
        for x in range(0,width,denom):
            if (binStr[(int(x/denom)+int(y/denom)*int(width/denom))] == '1'):
                img.paste(im, (x,y), im)
    
    img.save((os.path.splitext(ntpath.basename(imageName))[0])+'background.png')

def makeImgMulti(width, height, binaryfile, zipName):
    imgs = [] #16 image slots
    with open(binaryfile, 'r') as file:
        binStr = file.read().replace('\n', '')
    
    #extract to a temp path with name of the archive
    path = os.path.dirname(zipName)
    zipFolder = os.path.splitext(zipName)[0]

    with ZipFile(zipName, 'r') as zip:
        for item in zip.namelist():
            if (item.endswith(".png")):
                zip.extract(item, path)

    if not (os.path.exists(zipFolder+"/0.png")):
        print("Must have atleast base image 0.png in the zip")
        quit()

    #sets all components to the base image 
    for i in range(16):
        imgs.append(Image.open(zipFolder+"/0.png"))
    
    for item in os.listdir(zipFolder):
        if item.endswith(".png"):
            try:
                i = int((os.path.splitext(ntpath.basename(item))[0]))
            except ValueError:
                print("all files must have an integer name from 0-15 only!")
                quit()
            if(i>15 or i<0):
                print("all files must have an integer name from 0-15 only!")
                quit()
            imgs[i] = Image.open(zipFolder+"/"+item)

    print("Creating image height:", height, "width", width, "using zip", ntpath.basename(zipName))
    denom = imgs[0].size[0]
    for im in imgs:
        if (im.size[0] != im.size[1] or im.size[0] != denom):
            print("image ", im.name, " not square or has a different size than previous images")
            quit()

    if (width%denom != 0 or height%denom != 0):
        print("size of image does not evenly go into width or height")
        quit()
        
    while (len(binStr) < int((width/denom)*(height/denom))):
        binStr += binStr

    img = Image.new('RGB', (width, height), color = 'white')
    img.putalpha(0)
    x = 0
    y = 0
    for y in range(0,height,denom):
        for x in range(0,width,denom):
            if (binStr[(int(x/denom)+int(y/denom)*int(width/denom))] == '1'):
                #neighborIndex stores indexs locations for all the neighbors
                #they are stored in the order 0 - up, 1 - right, 2 - left, 3 - down
                imageVal = 0 #what image should be pasted at this location?
                neighborIndex = []
                neighborIndex.append((int(x/denom)+(int(y/denom)-1)*int(width/denom))) # up
                neighborIndex.append((int(x/denom)+int(y/denom)*int(width/denom))+1) # right
                neighborIndex.append((int(x/denom)+int(y/denom)*int(width/denom))-1) # left
                neighborIndex.append((int(x/denom)+(int(y/denom)+1)*int(width/denom))) # down
                #wrap edge cases
                for i in range(4):
                    if(neighborIndex[i]>=len(binStr)):
                        #too long wrap backwards
                        neighborIndex[i] -= len(binStr)
                    elif(neighborIndex[i]<0):
                        #too short, wrap positive
                        neighborIndex[i] += len(binStr)

                if(binStr[neighborIndex[0]] == '1'):
                    imageVal += 8
                if(binStr[neighborIndex[1]] == '1'):
                    imageVal += 4
                if(binStr[neighborIndex[2]] == '1'):
                    imageVal += 2
                if(binStr[neighborIndex[3]] == '1'):
                    imageVal += 1

                img.paste(imgs[imageVal], (x,y), imgs[imageVal])

    #cleanup time 
    shutil.rmtree(zipFolder)
    img.save((os.path.splitext(ntpath.basename(zipName))[0])+'background.png')

if (len(sys.argv)<4):
    print("please enter 4 commands in this order: #width #height #pathBinaryTextFile #pathToImageFile")
    print("or 3 commands without a pathToImageFile to create an image for each file in the \"patterns\" folder")
    quit()
if (len(sys.argv)==4):
    gWidth = int(sys.argv[1]) #2070
    gHeight = int(sys.argv[2]) #1170
    gBinaryfile = sys.argv[3]
    for filename in os.listdir("patterns/"):
        if filename.endswith(".png"):
            makeImg(gWidth, gHeight, gBinaryfile, "patterns/"+filename)
        elif(filename.endswith(".zip")):
            makeImgMulti(gWidth, gHeight, gBinaryfile, "patterns/"+filename)
else:
    gWidth = int(sys.argv[1]) #2070
    gHeight = int(sys.argv[2]) #1170
    gBinaryfile = sys.argv[3]
    gImageName = sys.argv[4] #"pattern30.png")
    if (gImageName.endswith(".png")):
        makeImg(gWidth, gHeight, gBinaryfile, gImageName)
    elif(gImageName.endswith(".zip")):
        makeImgMulti(gWidth, gHeight, gBinaryfile, gImageName)
