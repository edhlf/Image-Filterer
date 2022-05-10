#pyinstaller "C:\repository for Visual\pythonImgFilter\pythonImgFilter\pythonImgFilter.py" in powershell compiles it nicly
import numpy as np   
import PIL #meh, I'll import all for now
import pygame
import tkinter as tk
from tkinter import filedialog
from matplotlib import image
from matplotlib import pyplot
#from matplotlib.pyplot import ion
import time
import math
import random

pygame.init()
pyplot.axis('off')
pyplot.grid(b=None)
pyplot.tight_layout(pad=0.0, w_pad=0.0, h_pad=0.0)

pyplot.gca().set_axis_off()

pyplot.margins(0,0)
pyplot.gca().xaxis.set_major_locator(pyplot.NullLocator())
pyplot.gca().yaxis.set_major_locator(pyplot.NullLocator())

#pyplot.savefig("fileOut.PNG", bbox_inches = 'tight', pad_inches = 0)
#pyplot.savefig("fileOut.svg", format='svg', transparent=True, dpi=1200, pad_inches = 0)

#ion()
WIDTH = 640
HEIGHT = 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))

RED = (255,0,0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)
 
FONT = pygame.font.SysFont('timesnewroman',  30)

class pygameLogic:
    def __init__(self):
        self.background_colour = (255,255,255,0)
        self.run = 1

        self.FilterMode = -1

        self.B1 = FONT.render('L-Fringe', True, GREEN, BLUE)
        self.B2 = FONT.render('H-Dark', True, GREEN, BLUE)
        self.B3 = FONT.render('Pixelate', True, GREEN, BLUE)
        self.B4 = FONT.render('StencilH', True, GREEN, BLUE)
        
        self.B5 = FONT.render('Dramatize', True, GREEN, BLUE)
        self.B6 = FONT.render('PixDither', True, GREEN, BLUE)
        self.B7 = FONT.render('StencilV', True, GREEN, BLUE)
        self.B8 = FONT.render('Simple Inv.', True, GREEN, BLUE)

        self.B9 = FONT.render('StencilD', True, GREEN, BLUE)
        self.B10 = FONT.render('Sonic', True, GREEN, BLUE)
        self.B11 = FONT.render('RandStenH', True, GREEN, BLUE)
        self.B12 = FONT.render('RandStenV', True, GREEN, BLUE)
        
        self.B13 = FONT.render('S-Noise', True, GREEN, BLUE)
        self.B14 = FONT.render('GreyScale', True, GREEN, BLUE)
        self.B15 = FONT.render('GreyGrain', True, GREEN, BLUE)
        self.B16 = FONT.render('AllGrain', True, GREEN, BLUE)

        self.B17 = FONT.render('Box Flip', True, GREEN, BLUE)
        self.B18 = FONT.render('GlassShot', True, GREEN, BLUE)
        self.B19 = FONT.render('Flake', True, GREEN, BLUE)
        self.B20 = FONT.render('Swiped', True, GREEN, BLUE)



        self.D1 = FONT.render('ONLY RGB images - do not use PNG', True, GREEN, (0,0,0,0))
        self.D2 = FONT.render('saves in program dir; click cartridge to save again!', True, GREEN, (0,0,0,0))
        self.D3 = FONT.render('It can take time to load the image filter!', True, GREEN, (0,0,0,0))
        self.D4 = FONT.render('Close the extra window and right click to go back', True, GREEN, (0,0,0,0))

        self.pos = (0,0)

        self.NeedImage = 0 # start image loader as false
        self.FileChosen = ""
        self.imageData = list()
        self.ShowBool = 0
        self.tick = 0 #used for delay to allow pygame to have time to finish draw call to screen... did not find a way to check if a draw call is in progress, so I just chosen to tick 10 frames - since then I will be safe for most hardware

    def FilterBoxFlip(self):
        self.imageData.append(np.asarray(np.copy(self.imageData[0])))
        
        self.imageData.append(np.asarray(np.copy(self.imageData[0])))

        for i in range(0,len(self.imageData[1]),50): # y
            
            for ii in range(0,len(self.imageData[1][i]),50): #tuple of row - x of image
                if(i+50<len(self.imageData[1]) and ii+50 < len(self.imageData[1][i])):
                    for x in range(49,0, -1):
                        for y in range(49,0, -1):
                            arr = np.array([self.imageData[2][i+x][ii+y][0], self.imageData[2][i+x][ii+y][1], self.imageData[2][i+x][ii+y][2]])
                            self.imageData[1][i+(49-x)][ii+(49-y)] = arr

                #else:
                    #for x in range(0,49):
                    #    for y in range(0,49):


        pyplot.imshow(PIL.Image.fromarray(self.imageData[1])) #overrides... but meh for now
        return self

    def FilterGlassShot(self):
        self.imageData.append(np.asarray(np.copy(self.imageData[0])))
        
        self.imageData.append(np.asarray(np.copy(self.imageData[0])))

        for i in range(len(self.imageData[1])): # y
            for ii in range(len(self.imageData[1][i])): #tuple of row - x of image
                if(i<len(self.imageData[1])-101 and ii<len(self.imageData[1][i])-101 ):
                    arr = np.array([self.imageData[2][i+random.randint(50,100)][ii+random.randint(50,100)][0], self.imageData[2][i+random.randint(50,100)][ii+random.randint(50,100)][1], self.imageData[2][i+random.randint(50,100)][ii+random.randint(50,100)][2]])
                    self.imageData[1][i][ii] = arr
                else:
                    arr = np.array([self.imageData[1][i-random.randint(50,100)][ii-random.randint(50,100)][0], self.imageData[1][i-random.randint(50,100)][ii-random.randint(50,100)][1], self.imageData[1][i-random.randint(50,100)][ii-random.randint(50,100)][2]])
                    self.imageData[1][i][ii] = arr

                

        pyplot.imshow(PIL.Image.fromarray(self.imageData[1])) #overrides... but meh for now
        return self

    def FilterSoftFlake(self):
        self.imageData.append(np.asarray(np.copy(self.imageData[0])))
        arrX = list()
        arrY = list()
        TmpRand = random.randint(0,int(len(self.imageData[1])/2))
        for i in range(0,len(self.imageData[1])-TmpRand):
            arrY.append(random.randint(0,int(len(self.imageData[1]))))
        TmpRand = random.randint(0,int(len(self.imageData[1][0])/2))
        for i in range(0,len(self.imageData[1][0])-TmpRand): # lazy math
            arrX.append(random.randint(0,int(len(self.imageData[1][0]))))

        if(len(arrY)<len(arrX)):
            for i in range(len(arrY)): # y
                arr = np.array([255-self.imageData[1][arrY[i]][arrX[i]][0]*0.1, 255-self.imageData[1][arrY[i]][arrX[i]][1]*0.1, 255-self.imageData[1][arrY[i]][arrX[i]][2]*0.1])
                self.imageData[1][arrY[i]][arrX[i]] = arr
        else:
            for i in range(len(arrX)): # y
                arr = np.array([255-self.imageData[1][arrY[i]][arrX[i]][0]*0.1, 255-self.imageData[1][arrY[i]][arrX[i]][1]*0.1, 255-self.imageData[1][arrY[i]][arrX[i]][2]*0.1])
                self.imageData[1][arrY[i]][arrX[i]] = arr

        pyplot.imshow(PIL.Image.fromarray(self.imageData[1])) #overrides... but meh for now
        return self

    def FilterSwiped(self):
        self.imageData.append(np.asarray(np.copy(self.imageData[0])))
        for i in range(0,len(self.imageData[1]),2): # y
            for ii in range(0,len(self.imageData[1][i]),2): #tuple of row - x of image
                if(i+1<len(self.imageData[1]) and i+1<len(self.imageData[1][i])):
                    arr = np.array([255-self.imageData[1][i][ii][0], 255-self.imageData[1][i][ii][1], 255-self.imageData[1][i][ii][2]])
                    self.imageData[1][i][ii] = arr


        pyplot.imshow(PIL.Image.fromarray(self.imageData[1])) #overrides... but meh for now
        return self


    def FilterAllGrain(self):
        self.imageData.append(np.asarray(np.copy(self.imageData[0])))
        for i in range(len(self.imageData[1])): # y
            for ii in range(len(self.imageData[1][i])): #tuple of row - x of image
                maxVal = max(self.imageData[1][i][ii])
                if(maxVal-min(self.imageData[1][i][ii])<80):
                    arr = np.array([self.imageData[1][i][ii][0]*(random.randint(100,130)/100), self.imageData[1][i][ii][1]*(random.randint(100,130)/100), self.imageData[1][i][ii][2]*(random.randint(100,130)/100)])
                    self.imageData[1][i][ii] = arr
                else:
                    arr = np.array([self.imageData[1][i][ii][0],self.imageData[1][i][ii][1],self.imageData[1][i][ii][2]])
                    self.imageData[1][i][ii] = arr
        pyplot.imshow(PIL.Image.fromarray(self.imageData[1])) #overrides... but meh for now
        return self

    def FilterGreyGrain(self):
        self.imageData.append(np.asarray(np.copy(self.imageData[0])))
        for i in range(len(self.imageData[1])): # y
            for ii in range(len(self.imageData[1][i])): #tuple of row - x of image
                maxVal = max(self.imageData[1][i][ii])
                if(maxVal-min(self.imageData[1][i][ii])<80):
                    arr = np.array([maxVal*(random.randint(100,130)/100), maxVal*(random.randint(100,130)/100), maxVal*(random.randint(100,130)/100)])
                    self.imageData[1][i][ii] = arr
                else:
                    arr = np.array([maxVal, maxVal, maxVal])
                    self.imageData[1][i][ii] = arr

        pyplot.imshow(PIL.Image.fromarray(self.imageData[1])) #overrides... but meh for now
        return self

    def FilterGreyScale(self):
        self.imageData.append(np.asarray(np.copy(self.imageData[0])))
        for i in range(len(self.imageData[1])): # y
            for ii in range(len(self.imageData[1][i])): #tuple of row - x of image
                if(int(self.imageData[1][i][ii][0]) + int(self.imageData[1][i][ii][1]) + int(self.imageData[1][i][ii][2]) <400):
                    minVal = min(self.imageData[1][i][ii])
                    arr = np.array([minVal, minVal, minVal])
                    self.imageData[1][i][ii] = arr

                else:
                    maxVal = max(self.imageData[1][i][ii])
                    arr = np.array([maxVal, maxVal, maxVal])
                    self.imageData[1][i][ii] = arr

        pyplot.imshow(PIL.Image.fromarray(self.imageData[1])) #overrides... but meh for now
        return self


    def FilterSmartNoise(self):
        self.imageData.append(np.asarray(np.copy(self.imageData[0])))
        for i in range(len(self.imageData[1])): # y
            for ii in range(len(self.imageData[1][i])): #tuple of row - x of image
                val = random.randint(0,5)
                if(val == 1):
                    arr = np.array([self.imageData[1][i][ii][0]*(random.randint(20,100)/100), self.imageData[1][i][ii][1]*(random.randint(20,100)/100), self.imageData[1][i][ii][2]*(random.randint(20,100)/100)])
                    self.imageData[1][i][ii] = arr
                if(int(self.imageData[1][i][ii][0]) + int(self.imageData[1][i][ii][1]) + int(self.imageData[1][i][ii][2]) < random.randint(350,550)):
                    arr = np.array([self.imageData[1][i][ii][0]*(random.randint(20,100)/100), self.imageData[1][i][ii][1]*(random.randint(20,100)/100), self.imageData[1][i][ii][2]*(random.randint(20,100)/100)])
                    self.imageData[1][i][ii] = arr
                        
                else:
                    arr = np.array([self.imageData[1][i][ii][0]*(random.randint(100,105)/100), self.imageData[1][i][ii][1]*(random.randint(100,105)/100), self.imageData[1][i][ii][2]*(random.randint(100,105)/100)])
                    self.imageData[1][i][ii] = arr


        pyplot.imshow(PIL.Image.fromarray(self.imageData[1])) #overrides... but meh for now
        return self

    def FilterRandStencilH(self):
        self.imageData.append(np.asarray(np.copy(self.imageData[0])))

        for i in range(len(self.imageData[1])): # y
            for ii in range(len(self.imageData[1][i])): #tuple of row - x of image
                if(int(self.imageData[1][i][ii][0]) + int(self.imageData[1][i][ii][1]) + int(self.imageData[1][i][ii][2]) < random.randint(350,550)):
                    if(i%2 == 0):
                        arr = np.array([self.imageData[1][i][ii][0]*(random.randint(20,100)/100), self.imageData[1][i][ii][1]*(random.randint(20,100)/100), self.imageData[1][i][ii][2]*(random.randint(20,100)/100)])
                        self.imageData[1][i][ii] = arr
                        
                    else:
                        arr = np.array([self.imageData[1][i][ii][0]*(random.randint(100,105)/100), self.imageData[1][i][ii][1]*(random.randint(100,105)/100), self.imageData[1][i][ii][2]*(random.randint(100,105)/100)])
                        self.imageData[1][i][ii] = arr
                        
                            
        pyplot.imshow(PIL.Image.fromarray(self.imageData[1])) #overrides... but meh for now
        return self

    def FilterRandStencilV(self):
        self.imageData.append(np.asarray(np.copy(self.imageData[0])))
        
        for i in range(len(self.imageData[1])): # y
        
            for ii in range(len(self.imageData[1][i])): #tuple of row - x of image
                    if(int(self.imageData[1][i][ii][0]) + int(self.imageData[1][i][ii][1]) + int(self.imageData[1][i][ii][2]) < random.randint(350,550)):
                        if(ii%2 == 0):
                            arr = np.array([self.imageData[1][i][ii][0]*(random.randint(20,100)/100), self.imageData[1][i][ii][1]*(random.randint(20,100)/100), self.imageData[1][i][ii][2]*(random.randint(20,100)/100)])
                            self.imageData[1][i][ii] = arr
                        
                        else:
                            arr = np.array([self.imageData[1][i][ii][0]*(random.randint(100,105)/100), self.imageData[1][i][ii][1]*(random.randint(100,105)/100), self.imageData[1][i][ii][2]*(random.randint(100,105)/100)])
                            self.imageData[1][i][ii] = arr
        pyplot.imshow(PIL.Image.fromarray(self.imageData[1])) #overrides... but meh for now
        return self      
                            
    def FilterSonic(self): #flip every other pixel

        self.imageData.append(np.asarray(np.copy(self.imageData[0])))

        for i in range(len(self.imageData[1])): # y
            for ii in range(len(self.imageData[1][i])): #tuple of row - x of image
                yRatio = i/len(self.imageData[1])
                xRatio = ii/len(self.imageData[1][0])
                if(yRatio*xRatio>0.3 and yRatio*xRatio<0.8 and i%3==0 and ii%3==0):
                    arr = np.array([self.imageData[1][i][ii][0]*0.2, self.imageData[1][i][ii][1]*0.2, self.imageData[1][i][ii][2]*2])
                    self.imageData[1][i][ii] = arr
                
        pyplot.imshow(PIL.Image.fromarray(self.imageData[1])) #overrides... but meh for now
        return self

    def FilterStencilD(self): #flip every other pixel

        self.imageData.append(np.asarray(np.copy(self.imageData[0])))

        for i in range(len(self.imageData[1])): # y
            for ii in range(len(self.imageData[1][i])): #tuple of row - x of image
                if(i%4-ii%4==0 and (int(self.imageData[1][i][ii][0]) + int(self.imageData[1][i][ii][1]) + int(self.imageData[1][i][ii][2]) < 400)==0):
                    arr = np.array([self.imageData[1][i][ii][0]*0.2, self.imageData[1][i][ii][1]*0.2, self.imageData[1][i][ii][2]*0.2])
                    self.imageData[1][i][ii] = arr
                
        pyplot.imshow(PIL.Image.fromarray(self.imageData[1])) #overrides... but meh for now
        return self


    def FilterInverseBase(self):

        self.imageData.append(np.asarray(np.copy(self.imageData[0])))

        for i in range(len(self.imageData[1])): # y
            for ii in range(len(self.imageData[1][i])): #tuple of row - x of image
                arr = np.array([255-self.imageData[1][i][ii][0], 255-self.imageData[1][i][ii][1], 255-self.imageData[1][i][ii][2]])
                self.imageData[1][i][ii] = arr
                
        pyplot.imshow(PIL.Image.fromarray(self.imageData[1])) #overrides... but meh for now
        return self

    def FilterPixelDither(self):
        self.imageData.append(np.asarray(np.copy(self.imageData[0])))
        #sets 5 pixels around 1 pixel the same as the 1 pixel - makes a pixalate color style
        for i in range(int(len(self.imageData[1])/3)-1): # y
            for ii in range(int(len(self.imageData[1][i])/3)-1): #tuple of row - x of image
                #if(int(self.imageData[1][i*5][ii*5][0]) + int(self.imageData[1][i*5][ii*5][1]) + int(self.imageData[1][i*5][ii*%][2]) < 400):
                    
                    
                arr1 = np.array([self.imageData[1][i*3][ii*3][0]+10, self.imageData[1][i*3][ii*3][1]-10, self.imageData[1][i*3][ii*3][2]+10])
                arr2 = np.array([self.imageData[1][i*3][ii*3][0]-10, self.imageData[1][i*3][ii*3][1]-10, self.imageData[1][i*3][ii*3][2]-10])
                arr3 = np.array([self.imageData[1][i*3][ii*3][0]-10, self.imageData[1][i*3][ii*3][1]+10, self.imageData[1][i*3][ii*3][2]+10])
                
                
                if (i*3+1<len(self.imageData[1]) and ii*3-1<0):
                    self.imageData[1][i*3+1][ii*3-1] = arr1
                if (i*3-1>0 and ii*3+1>len(self.imageData[1][0])):
                    self.imageData[1][i35-1][ii*3+1] = arr3
                if (i*3-1>0 and ii*3-1>0):
                    self.imageData[1][i*3-1][ii*3-1] = arr2
                if (i*3-1>0):
                    self.imageData[1][i*3-1][ii*3] = arr1
                if (ii*3-1>0):
                    self.imageData[1][i*3][ii*3-1] = arr3
                if (i*3+1<len(self.imageData[1])):
                    self.imageData[1][i*3+1][ii*3] = arr2
                if (ii*3+1<len(self.imageData[1][i*3])):
                    self.imageData[1][i*3][ii*3+1] = arr1
                if (i*3+1<len(self.imageData[1]) and ii*3+1<len(self.imageData[1][i*3])):
                    self.imageData[1][i*3+1][ii*3+1] = arr3

                    #refrence y and then x axis

        pyplot.imshow(PIL.Image.fromarray(self.imageData[1])) #overrides... but meh for now
        return self
   
    def FilterDramatize(self):

        self.imageData.append(np.asarray(np.copy(self.imageData[0])))

        for i in range(len(self.imageData[1])): # y
            for ii in range(len(self.imageData[1][i])): #tuple of row - x of image
                if(int(self.imageData[1][i][ii][0]) + int(self.imageData[1][i][ii][1]) + int(self.imageData[1][i][ii][2]) > 600):
                    arr = np.array([self.imageData[1][i][ii][0]*1.1, self.imageData[1][i][ii][1]*1.1, self.imageData[1][i][ii][2]*1.1])
                    self.imageData[1][i][ii] = arr
                elif(int(self.imageData[1][i][ii][0]) + int(self.imageData[1][i][ii][1]) + int(self.imageData[1][i][ii][2]) < 300):
                    arr = np.array([self.imageData[1][i][ii][0]*0.2, self.imageData[1][i][ii][1]*0.2, self.imageData[1][i][ii][2]*0.2])
                    self.imageData[1][i][ii] = arr
                
        pyplot.imshow(PIL.Image.fromarray(self.imageData[1])) #overrides... but meh for now
        return self

    def FilterBrightFrizz(self):
        self.imageData.append(np.asarray(np.copy(self.imageData[0])))

        

        #data = np.fromstring(self.imageData[0].tostring_rgb(), dtype=np.uint8, sep='') #forces to RGB... don't think I care... who needs alpha any ways ... but I will still work around alpha in areas in case it remotely matters... not like I need to over eng stuff
        #data = data.reshape(self.imageData[0].get_width_height()[::-1] + (3,))

        #self.imageData.append(data)

        for i in range(len(self.imageData[1])): # y
            for ii in range(len(self.imageData[1][i])): #tuple of row - x of image
                 #r,g,b,a <-- alpha may not be present, if using you MUST check for alpha - also always modify in such a way that it is safe for alph and non alpha containing images
                #YOU MUST CAST ALL VALUES TO AN INT else they are a u8 --> 8 bits is going to overflow and not work as intended
                if(int(self.imageData[1][i][ii][0]) + int(self.imageData[1][i][ii][1]) + int(self.imageData[1][i][ii][2]) > 500):
                    arr = np.array([self.imageData[1][i][ii][0]*1.2, self.imageData[1][i][ii][1]*1.2, self.imageData[1][i][ii][2]*1.2])
                    self.imageData[1][i][ii] = arr
                    #refrence y and then x axis

        pyplot.imshow(PIL.Image.fromarray(self.imageData[1])) #overrides... but meh for now
        return self

    def FilterHDark(self):
        self.imageData.append(np.asarray(np.copy(self.imageData[0])))

        for i in range(len(self.imageData[1])): # y
            for ii in range(len(self.imageData[1][i])): #tuple of row - x of image
                if(int(self.imageData[1][i][ii][0]) + int(self.imageData[1][i][ii][1]) + int(self.imageData[1][i][ii][2]) < 400):
                    arr = np.array([self.imageData[1][i][ii][0]*0.3, self.imageData[1][i][ii][1]*0.3, self.imageData[1][i][ii][2]*0.3])
                    self.imageData[1][i][ii] = arr
                    #refrence y and then x axis

        pyplot.imshow(PIL.Image.fromarray(self.imageData[1])) #overrides... but meh for now
        return self

    def FilterStencilH(self):
        self.imageData.append(np.asarray(np.copy(self.imageData[0])))

        for i in range(len(self.imageData[1])): # y
            for ii in range(len(self.imageData[1][i])): #tuple of row - x of image
                if(int(self.imageData[1][i][ii][0]) + int(self.imageData[1][i][ii][1]) + int(self.imageData[1][i][ii][2]) < 400):
                    if(i%2 == 0):
                        arr = np.array([self.imageData[1][i][ii][0]*0.2, self.imageData[1][i][ii][1]*0.2, self.imageData[1][i][ii][2]*0.2])
                        self.imageData[1][i][ii] = arr
                        
                    else:
                        arr = np.array([self.imageData[1][i][ii][0]*1.2, self.imageData[1][i][ii][1]*1.2, self.imageData[1][i][ii][2]*1.2])
                        self.imageData[1][i][ii] = arr
                        
                            
        pyplot.imshow(PIL.Image.fromarray(self.imageData[1])) #overrides... but meh for now
        return self

    def FilterStencilV(self):
        self.imageData.append(np.asarray(np.copy(self.imageData[0])))

        for i in range(len(self.imageData[1])): # y
            for ii in range(len(self.imageData[1][i])): #tuple of row - x of image
                if(int(self.imageData[1][i][ii][0]) + int(self.imageData[1][i][ii][1]) + int(self.imageData[1][i][ii][2]) < 400):
                    if(ii%2 == 0):
                        arr = np.array([self.imageData[1][i][ii][0]*0.2, self.imageData[1][i][ii][1]*0.2, self.imageData[1][i][ii][2]*0.2])
                        self.imageData[1][i][ii] = arr
                        
                    else:
                        arr = np.array([self.imageData[1][i][ii][0]*1.2, self.imageData[1][i][ii][1]*1.2, self.imageData[1][i][ii][2]*1.2])
                        self.imageData[1][i][ii] = arr
                        
                            
        pyplot.imshow(PIL.Image.fromarray(self.imageData[1])) #overrides... but meh for now
        return self


    def FilterPixelate(self):
        self.imageData.append(np.asarray(np.copy(self.imageData[0])))
        #sets 5 pixels around 1 pixel the same as the 1 pixel - makes a pixalate color style
        for i in range(int(len(self.imageData[1])/3)-1): # y
            for ii in range(int(len(self.imageData[1][i])/3)-1): #tuple of row - x of image
                #if(int(self.imageData[1][i*5][ii*5][0]) + int(self.imageData[1][i*5][ii*5][1]) + int(self.imageData[1][i*5][ii*%][2]) < 400):
                    
                    
                arr = np.array([self.imageData[1][i*3][ii*3][0], self.imageData[1][i*3][ii*3][1], self.imageData[1][i*3][ii*3][2]])
                
                
                if (i*3+1<len(self.imageData[1]) and ii*3-1<0):
                    self.imageData[1][i*3+1][ii*3-1] = arr
                if (i*3-1>0 and ii*3+1>len(self.imageData[1][0])):
                    self.imageData[1][i35-1][ii*3+1] = arr
                if (i*3-1>0 and ii*3-1>0):
                    self.imageData[1][i*3-1][ii*3-1] = arr
                if (i*3-1>0):
                    self.imageData[1][i*3-1][ii*3] = arr
                if (ii*3-1>0):
                    self.imageData[1][i*3][ii*3-1] = arr
                if (i*3+1<len(self.imageData[1])):
                    self.imageData[1][i*3+1][ii*3] = arr
                if (ii*3+1<len(self.imageData[1][i*3])):
                    self.imageData[1][i*3][ii*3+1] = arr
                if (i*3+1<len(self.imageData[1]) and ii*3+1<len(self.imageData[1][i*3])):
                    self.imageData[1][i*3+1][ii*3+1] = arr

                    #refrence y and then x axis

        pyplot.imshow(PIL.Image.fromarray(self.imageData[1])) #overrides... but meh for now
        return self

    def SelectButton(self):
        #choose a button to filter with

        pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, HEIGHT) )
        pygame.draw.rect(screen, RED, (140, 0, 10, HEIGHT-30) ) 
        pygame.draw.rect(screen, RED, (290, 0, 10, HEIGHT) ) 
        pygame.draw.rect(screen, RED, (440, 0, 10, HEIGHT) ) 
        pygame.draw.rect(screen, RED, (600, 0, 50, HEIGHT) ) 
        
        add = 1
        pygame.draw.rect(screen, RED, (0, self.B1.get_height(), WIDTH, 5) ) 
        
        screen.blit(self.D3, (0,HEIGHT-30))

        screen.blit(self.B1, (0,0))

        screen.blit(self.B2, (150,0))
        
        screen.blit(self.B3, (300,0))

        screen.blit(self.B4, (450,0))
        
        add+=1
        pygame.draw.rect(screen, RED, (0, self.B1.get_height()*add+5*add, WIDTH+5, 5) ) 

        screen.blit(self.B5,(0,self.B1.get_height()*(add-1)+5))

        screen.blit(self.B6,(150,self.B1.get_height()*(add-1)+5))

        screen.blit(self.B7,(300,self.B1.get_height()*(add-1)+5))

        screen.blit(self.B8,(450,self.B1.get_height()*(add-1)+5))

        add+=1

        pygame.draw.rect(screen, RED, (0, self.B1.get_height()*add+5*add, WIDTH, 5) ) 

        screen.blit(self.B9,(0,self.B1.get_height()*(add-1)+5*add))

        screen.blit(self.B10,(150,self.B1.get_height()*(add-1)+5*add))

        screen.blit(self.B11,(300,self.B1.get_height()*(add-1)+5*add))

        screen.blit(self.B12,(450,self.B1.get_height()*(add-1)+5*add))

        add+=1

        pygame.draw.rect(screen, RED, (0, self.B1.get_height()*add+5*add, WIDTH, 5) ) 

        screen.blit(self.B13,(0,self.B1.get_height()*(add-1)+5*add))

        screen.blit(self.B14,(150,self.B1.get_height()*(add-1)+5*add))

        screen.blit(self.B15,(300,self.B1.get_height()*(add-1)+5*add))

        screen.blit(self.B16,(450,self.B1.get_height()*(add-1)+5*add))

        add+=1

        pygame.draw.rect(screen, RED, (0, self.B1.get_height()*add+5*add, WIDTH, 5) ) 

        screen.blit(self.B17,(0,self.B1.get_height()*(add-1)+5*add))

        screen.blit(self.B18,(150,self.B1.get_height()*(add-1)+5*add))

        screen.blit(self.B19,(300,self.B1.get_height()*(add-1)+5*add))

        screen.blit(self.B20,(450,self.B1.get_height()*(add-1)+5*add))


        if(pygame.mouse.get_pressed()[0] == 1): # index 0 is left click - true means clicked 

            #split y and x into 5's --> every 
            if(pygame.mouse.get_pos()[1]<self.B1.get_height()*(add-1)+5*add+35 and pygame.mouse.get_pos()[0]<600): #limit based on implemented filter button positions
                NormalizedY = math.floor(pygame.mouse.get_pos()[1]/5)
                NormalizedX = math.floor(pygame.mouse.get_pos()[0]/5)
                #self.FilterMode = NormalizedY/INTERVALS *4  + NromalizedX
            
            
                #- this path of code normalizes values so it is efficent to click anywhere - better than if else by magnitudes - since its only a bit of math
                if((NormalizedY!=0 and NormalizedY%8!=0) and (NormalizedY!=7)):#every 7 is a button on the vertical, and then you have 1 block of red, then 7 more of something, then 1 red - so if %8 is 0, we cannot click unless normalized y is 0 for edge case of == 0
                
                    if((NormalizedX%30 != 28 and NormalizedX%30!=29)): #28-29 rem which is really 29-30 - 2 is red box 
                        self.FilterMode = math.floor(NormalizedY/8) * 4  + math.floor(NormalizedX/32)

        return self
    
    def SelectImage(self):
        root = tk.Tk()
        root.withdraw()
        
        NotDone  = 1

        files = filedialog.askopenfilenames() #Not fully pausing runtime
        self.NeedImage = 1
        while NotDone == 1:
            if (len(files) != 0):
                break
            else:
                files = filedialog.askopenfilenames() 

        self.FileChosen = files[0]  #store it for future refrence if needded*

        imageD = image.imread(self.FileChosen)

        if(len(imageD[0][0])==4):
            kill() #only RGB support

        self.imageData.append(imageD)

        #show OG image

        #pyplot.imshow(self.imageData[0]) <-- add back for comparison later?
        
        #remember to call pyplot.show() when done the other image processing
        
        return self
    def MainInstance(self):

        while self.run:

            screen.fill(self.background_colour)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = 0

            if (self.FilterMode == -1):
                self.SelectButton()
            else:   
                if (self.NeedImage == 0):
                    self.SelectImage()
                    #run image loader and make false once loaded image
                    #run filters
                    funcList = [self.FilterBrightFrizz,self.FilterHDark,self.FilterPixelate,self.FilterStencilH,self.FilterDramatize, self.FilterPixelDither, self.FilterStencilV, self.FilterInverseBase, self.FilterStencilD, self.FilterSonic, self.FilterRandStencilH, self.FilterRandStencilV, self.FilterSmartNoise, self.FilterGreyScale, self.FilterGreyGrain, self.FilterAllGrain, self.FilterBoxFlip, self.FilterGlassShot, self.FilterSoftFlake, self.FilterSwiped]
                    # ^ faster than if else...

                    funcList[self.FilterMode]()

                    self.ShowBool = 1
                    self.tick += 1
                else:
                    screen.blit(self.D1, (0,0))
                    screen.blit(self.D2, (0,35))
                    screen.blit(self.D3, (0,70))
                    screen.blit(self.D4, (0,300))

                    if (pygame.mouse.get_pressed()[2] == 1): #left click only ;P
                        self.tick = 0
                        self.FilterMode = -1
                        self.NeedImage = 0
                        self.FileChosen = ""
                        self.imageData = list()
                        self.ShowBool = 0
                        pyplot.axis('off')
                        pyplot.grid(b=None)
                        pyplot.tight_layout(pad=0.0, w_pad=0.0, h_pad=0.0)

                        pyplot.gca().set_axis_off()

                        pyplot.margins(0,0)
                        pyplot.gca().xaxis.set_major_locator(pyplot.NullLocator())
                        pyplot.gca().yaxis.set_major_locator(pyplot.NullLocator())

                    #TODO: add back button that resets var states and say you need to close
                    #TODO: add more filters
                    #TODO: ? I may want to make it look better
            pygame.display.update()
            
            if(self.tick!=0):
                self.tick+=1

            if(self.ShowBool and self.tick > 10):
                self.tick = 0
                pyplot.savefig("High resoltion.jpg",format ="jpg", dpi=150, bbox_inches='tight', transparent="True")
                pyplot.show()
                self.ShowBool = 0
#                pyplot.savefig('test.png', bbox_inches='tight',pad_inches = 0, dpi = 200)

        return self

PGI = pygameLogic()


PGI.MainInstance()
