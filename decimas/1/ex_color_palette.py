# coding=utf-8
"""
Daniel Calderon, CC3501, 2019-1
Indirect color example
"""

import numpy as np
import matplotlib.pyplot as mpl
import matplotlib.animation as animation


# Extract the different colors from an image
def getColorPalette(image):
    # 3 dimensions: row, column and color
    assert len(image.shape) == 3

    # color must have 3 components (RGB)
    assert image.shape[2] == 3

    # Here we will construct the indexed image, the index is only 8 bits long representing a positive integer number
    indexedImage = np.zeros(shape=(image.shape[0], image.shape[1]), dtype=np.uint8)

    # A helper dictionary to associate colors and indices easily
    colorsDict = {}
    # A list to associate indices and colors easily
    colorsPalette = []

    # Checking each row
    for i in range(image.shape[0]):
        # Checking each column
        for j in range(image.shape[1]):
            # The value image[i,j,X] corresponds to the pixel located at i,j.
            # X could be 0, 1 or 2, refering to the color component Read, Green or Blue respectively.
            # The color component value is float value between 0 and 1.

            # converting the numpy array into a python tuple, which can be used as index in a python dictionary
            pixelColor = (image[i, j, 0], image[i, j, 1], image[i, j, 2])

            # if the color is not in the palette, it is added
            if pixelColor not in colorsDict:
                # Getting an index for the new color
                colorIndex = len(colorsDict)
                # Storing the index in the dictionary for further queries
                colorsDict[pixelColor] = colorIndex
                # Storing the color associated with a given color index
                colorsPalette += [image[i, j, :]]

            # storing the index in the indexed image
            # print("pp", colorsDict, pixelColor)
            indexedImage[i, j] = colorsDict[pixelColor]

    # returning indexed image and its colors
    return indexedImage, colorsPalette


def assignColors(indexedImage, colorsPalette):
    # 2 dimensions: row and column
    assert len(indexedImage.shape) == 2

    # Here we will construct the image
    image = np.zeros(shape=(indexedImage.shape[0], indexedImage.shape[1], 3), dtype=np.float)

    # Checking each row
    for i in range(indexedImage.shape[0]):
        # Checking each column
        for j in range(indexedImage.shape[1]):
            # Painting the image with the color in the palette
            colorIndex = indexedImage[i, j]
            image[i, j, :] = colorsPalette[colorIndex]

    return image


def modifyPalette(colorPalette):
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


if __name__ == "__main__":
    # Reading an image into a numpy array
    originalImage = mpl.imread("santiago.png")

    print("Shape of the image: ", originalImage.shape)
    print("Example of pixel value:", originalImage[1, 2, :])

    # Obtaining all different colors in the image and the indexed image
    indexedImage, colorsPalette = getColorPalette(originalImage)

    # Modifying the color palette
    newColorPalette = modifyPalette(colorsPalette)

    # Reconstructing image
    reconstructedImage = assignColors(indexedImage, newColorPalette)

    # Arranging the original and modified images
    fig, axs = mpl.subplots(2, 1)
    axs[0].imshow(originalImage)
    axs[1].imshow(reconstructedImage)
    fig.suptitle('Indirect Color Example')

    # Displaying the figure
    mpl.show()
