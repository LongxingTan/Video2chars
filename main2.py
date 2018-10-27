#
from PIL import Image, ImageFont, ImageDraw
from moviepy.editor import *
import numpy as np

class video2chars():
    def __init__(self,input_name,output_name):
        self.input=input_name
        self.output=output_name
        self.ascii_char = "@WWMMHHBBRREEZZXXGG##LL***kkkknnnssssoooocccc++++----....."

    def pixel2chars(self,r, g, b, alpha=256):
        ''' map the grayscale 256 into 70 ascii characters  '''

        length = len(self.ascii_char)
        gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
        unit = (256.0 + 1) / length
        return self.ascii_char[int(gray / unit)]

    def frame2chars(self,img):
        font = ImageFont.truetype('./Arial.ttf', 10, encoding='unic')
        # font = ImageFont.load_default().font
        font_w, font_h = font.getsize(self.ascii_char[1])
        #font_w *= 1.5

        txt = ""
        colors = []
        width_raw=img.shape[1]
        height_raw=img.shape[0]
        width=int(width_raw//font_w)
        height=int(height_raw//font_h)
        img = Image.fromarray(img).resize((width,height), Image.NEAREST)

        for i in range(height):
            for j in range(width):
                pixel = img.getpixel((j, i))
                colors.append((pixel[0], pixel[1], pixel[2]))
                txt += self.pixel2chars(pixel[0], pixel[1], pixel[2])
            txt += '\n'
            colors.append((255, 255, 255))

        #with open("output.txt", 'w') as f:
            #f.write(txt)

        img_txt = Image.new("RGB", (width_raw, height_raw), (255, 255, 255))
        dr = ImageDraw.Draw(img_txt)
        x = y = 0
        for i in range(len(txt)):
            if (txt[i] == '\n'):
                x =0
                y += font_h
            else:
                dr.text((x, y), text=txt[i], font=font, fill=colors[i])
                x += font_w
        return np.array(img_txt)

    def movie2movie(self):
        videoclip = VideoFileClip(self.input)
        videoclip_txt=videoclip.fl_image(self.frame2chars)
        videoclip_txt.write_videofile(self.output)

    def frame2frame(self,file_name):
        from matplotlib import pyplot as plt
        import cv2
        img = cv2.imread(file_name)
        img = self.frame2chars(img)
        plt.imshow(img)
        plt.show()

if '__main__' == __name__:
    video = video2chars('video2.mp4', 'out2.mp4')
    video.movie2movie()
    #video.frame2frame('1.jpg')

