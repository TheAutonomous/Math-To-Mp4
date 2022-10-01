import shutil
from PIL import Image
from tqdm import tqdm
import cv2, math, os, glob
import moviepy.editor as moviepy

######## Requirements #######
#     pip install pillow    #
# pip install opencv-python #
#    pip install moviepy    #
#      pip install tqdm     #
#############################

# By TheAutonomous Btw ;) #

if not os.path.isdir("WorkingFolder"):
    os.mkdir("WorkingFolder")

try:
    os.remove("WorkingFolder/Frames")
    os.mkdir("WorkingFolder/Frames")
except:
    os.mkdir("WorkingFolder/Frames")

print("Frames Folder Refreshed")

class CustomMath():
    def RootPI(x):
        return math.cosh(x**2)*math.pi

def GenerateFrame(ScreenX, ScreenY):
    return Image.new('RGB', (ScreenX, ScreenY))

ScreenX = 1920
ScreenY = ScreenX
PixelSize = math.floor(ScreenX/100)
YPrecision = 20
XPrecision = 2
YDistort = math.floor(ScreenX/2)+YPrecision
EndFrameCount = 1000
StartFrameCount = 0
DoInvertedAxes = True
MathFunctionsToUse = [math.sin, math.cos, math.tan, CustomMath.RootPI]
FPS = 60.0

def GraphPoint(image, posx, posy, squaresize):
    for x in range(squaresize):
        for y in range(squaresize):
            image.putpixel((posx+x, posy+y), (255, 255, 255, 0))
    return image

def HandleGraph(x, y):
    global CImage
    CImage = GraphPoint(CImage, math.floor(x*PixelSize/XPrecision), math.floor(y*(YPrecision))+YDistort, PixelSize)

def toPositive(num):
    if num < 0:
        return num*-1
    else:
        return num

def MathFunctionToEnclose(cfunc, x, z):
    return math.sqrt(cfunc(x**2))*z

def HandleFrames():
    PDone = 0
    for z in range(StartFrameCount, EndFrameCount):
        global CImage
        CImage = GenerateFrame(ScreenX, ScreenY)
        for x in range(math.floor(ScreenX)):
            X = (x/XPrecision)
            X = X-X/2
            for i in MathFunctionsToUse:
                try:
                    y = MathFunctionToEnclose(i, X, z)
                    HandleGraph(x, y)
                except:
                    continue
                if DoInvertedAxes == True:
                    try:
                        y = -1*MathFunctionToEnclose(i, X, z)
                        HandleGraph(x, y)
                    except:
                        continue
        CImage.save("./WorkingFolder/Frames/" + str(z) + ".png")
        if z%((toPositive(StartFrameCount)+EndFrameCount)/10) == 0:
            PDone += 10
            print("Processing Frames Is " + str(PDone) + "% Done!")

def HandleVideo():
    image_folder = './WorkingFolder/Frames/*'
    video_name = './WorkingFolder/Finished.avi'
    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    video=cv2.VideoWriter(video_name,fourcc, FPS, (ScreenX,ScreenY))

    for i in tqdm((sorted(glob.glob(image_folder),key=os.path.getmtime))):
        video.write(cv2.imread(i))

    cv2.destroyAllWindows()
    video.release()
    clip = moviepy.VideoFileClip("./WorkingFolder/Finished.avi")
    clip.write_videofile("./WorkingFolder/Finished.mp4")
    try:
        os.remove('./WorkingFolder/Finished.avi')
        shutil.move('./WorkingFolder/Finished.mp4', './Finished.mp4')
        os.remove('WorkingFolder/Frames')
    except Exception as E:
        print(E)


if __name__ == '__main__':
    HandleFrames()
    HandleVideo()