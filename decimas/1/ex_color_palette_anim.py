# coding=utf-8
"""
Daniel Calderon, CC3501, 2019-1
Animation with indirect color
"""

from ex_color_palette import *

def getGreyScalePalette(colorPalette):
    newPalette = []
    for color in colorPalette:
        newNumber = np.mean(color)
        newColor = np.array([newNumber,newNumber,newNumber],dtype=np.float)
        newPalette += [newColor]
        print(newPalette)
    return newPalette

def getSepiaScalePalette(colorPalette):
    newPalette = []
    for color in colorPalette:
        newNumber = np.mean(color)
        newColor = np.array([newNumber*0.43,newNumber*0.25,newNumber*0.07],dtype=np.float)
        newPalette += [newColor]
    print(newPalette)
    return newPalette

def getNigthVisionScalePalette(colorPalette):
    newPalette = []
    for color in colorPalette:
        newNumber = np.mean(color)
        newColor = np.array([newNumber*0,newNumber*1,newNumber*0],dtype=np.float)
        newPalette += [newColor]
        print(newPalette)
    return newPalette

def getThermalVisionPalette(colorPalette):
    newPalette = []
    for color in colorPalette:
        # Generating a new color changing the RGB order...
        newNumber = (color[1] + color[2] + color[0]) / 3
        v1 = 0.2
        v2 = 0.4
        v3 = 0.8
        if newNumber < v1:
            newColor = np.array([0, 0, 1], dtype=np.float)
        elif newNumber < v2:
            newColor = np.array([1, 0, 0], dtype=np.float)
        elif newNumber < v3:
            newColor = np.array([1, 1, 0], dtype=np.float)
        else:
            newColor = np.array([1, 1, 1], dtype=np.float)
        newPalette += [newColor]
    return newPalette

def updatePalette(colorPalette, greyScalePalette, sepiaPallete, nigthVisionPalette, thermalVisionPalette, t):

    newPalette = []
    for i  in range(len(colorPalette)):
        if t<1:
            print(t)
            # Generating a new color changing the RGB order...
            newColor = np.array([
                colorPalette[i][0] * (1-t) + greyScalePalette[i][0] *t,
                colorPalette[i][1] * (1-t) + greyScalePalette[i][1] *t,
                colorPalette[i][2] * (1-t) + greyScalePalette[i][2] *t],
                dtype=np.float)
            newPalette += [newColor]
        if t<2 and t>1:
            print("sepia")
            t=t-1
            newColor = np.array([
                greyScalePalette[i][0] * (1 - t) + sepiaPallete[i][0] * t,
                greyScalePalette[i][1] * (1 - t) + sepiaPallete[i][1] * t,
                greyScalePalette[i][2] * (1 - t) + sepiaPallete[i][2] * t],
                dtype=np.float)
            newPalette += [newColor]
            t=t+1
        if t<3 and t>2:
            print("verde")
            t=t-2
            newColor = np.array([
                sepiaPallete[i][0] * (1 - t) + nigthVisionPalette[i][0] * t,
                sepiaPallete[i][1] * (1 - t) + nigthVisionPalette[i][1] * t,
                sepiaPallete[i][2] * (1 - t) + nigthVisionPalette[i][2] * t],
                dtype=np.float)
            newPalette += [newColor]
            t=t+2
        if t>3:
            print("vuelta")
            t=t-3
            newColor = np.array([
                nigthVisionPalette[i][0] * (1 - t) + thermalVisionPalette[i][0] * t,
                nigthVisionPalette[i][1] * (1 - t) + thermalVisionPalette[i][1] * t,
                nigthVisionPalette[i][2] * (1 - t) + thermalVisionPalette[i][2] * t],
                dtype=np.float)
            newPalette += [newColor]
            t=t+3
    return newPalette


if __name__ == "__main__":

    # Reading an image into a numpy array
    originalImage = mpl.imread("santiago.png")

    # Obtaining all different colors in the image and the indexed image
    indexedImage, colorPalette = getColorPalette(originalImage)
    greyScalePalette = getGreyScalePalette(colorPalette)
    SepiaPalette = getSepiaScalePalette(colorPalette)
    NigthVisionPallete = getNigthVisionScalePalette(colorPalette)
    thermalVisionPalette = getThermalVisionPalette(colorPalette)
    # Reconstructing image
    animatedImage = assignColors(indexedImage, colorPalette)


    fig, ax = mpl.subplots()
    im = ax.imshow(originalImage, animated=True)

    time = 0

    def updateFig(*args):
        global time
        global greyScalePalette
        global SepiaPalette
        global NigthVisionPallete
        global thermalVisionPalette
        time += 0.025
        param = 4*np.abs(np.sin(time))
        print(param)
        newColorPalette = updatePalette(colorPalette,greyScalePalette,SepiaPalette,NigthVisionPallete, thermalVisionPalette,
                                        param)
        updatedImage = assignColors(indexedImage, newColorPalette)
        im.set_array(updatedImage)
        return im,

    ani = animation.FuncAnimation(fig, updateFig, interval=100, blit=True)
    mpl.show()