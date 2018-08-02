from PIL import Image,ImageFont,ImageDraw
from moviepy.editor import VideoFileClip
import numpy as np
import matplotlib.pyplot as plt
import io
import textwrap

ascii_char = list("@WWMMHHBBRREEZZXXGG##LL***kkkknnnssssoooocccc++++----")

def get_char(r,g,b,alpha=256):
    ''' map the grayscale 256 into 70 ascii characters  '''
    if alpha==0:
        return ' '
    length=len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    unit = (256.0 + 1) / length
    return ascii_char[int(gray / unit)]

def image_process(img):
    '''the numpy type image is processed into char type image  '''
    #img = Image.open(img)
    img = Image.fromarray(img)
    WIDTH, HEIGHT= img.size
    WIDTH, HEIGHT=WIDTH//3, HEIGHT//3
    img = img.resize((WIDTH, HEIGHT), Image.NEAREST)

    text = ""
    for i in range(HEIGHT):
        for j in range(WIDTH):
            content = img.getpixel((j, i))
            text += get_char(*content)
        text += '\n'
    #with open("output.txt", 'w') as f:
        #f.write(text)

    text2image(text)

    fig = plt.figure(figsize=(12,16),dpi=100)
    plt.text(0, 0, text, fontsize=3)
    plt.axis('off')
    fig.canvas.draw()
    data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    return data

def image_process2(img):
    '''the numpy type image is processed into char type image  '''
    # img = Image.open(img)
    img = Image.fromarray(img)
    WIDTH, HEIGHT = img.size
    WIDTH, HEIGHT = WIDTH // 3, HEIGHT // 3
    img = img.resize((WIDTH, HEIGHT), Image.NEAREST)

    text = ""
    for i in range(HEIGHT):
        for j in range(WIDTH):
            content = img.getpixel((j, i))
            text += get_char(*content)
        text += '\n'
        # with open("output.txt", 'w') as f:
        # f.write(text)
    # https://stackoverflow.com/questions/7698231/python-pil-draw-multiline-text-on-image
    font = ImageFont.truetype('./Arial.ttf', 7, encoding='unic')
    image = Image.new('RGB', (WIDTH*5, HEIGHT*5), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    lines = textwrap.wrap(text, width=70)
    y_start = 0
    for i, line in enumerate(lines):
        width, height = font.getsize(line)
        draw.text((0, y_start), line, font=font, fill=(255, 0, 0))
        y_start += height
    return np.asarray(image)



def video_process(video,output):
    '''    The video is splited into pictures, and each picture is processed into char   '''
    clip1 = VideoFileClip(video)
    white_clip = clip1.fl_image(image_process2)  # NOTE: this function expects color images
    white_clip.write_videofile(output, audio=False)

def text2image(text):
    #https://stackoverflow.com/questions/7698231/python-pil-draw-multiline-text-on-image
    font = ImageFont.truetype('./Arial.ttf',7,encoding='unic')
    #text=text.decode('utf-8')
    img = Image.new('RGB', (300, 400),(255, 255, 255))
    draw = ImageDraw.Draw(img)
    lines=textwrap.wrap(text,width=300)
    #lines=text.split('\n')
    y_text=0
    for i,line in enumerate(lines):
        width,height=font.getsize(line)
        draw.text((0,y_text),line,font=font,fill=(255,0,0))
        y_text+=height


    #d = ImageDraw.Draw(img)
    #d.text((0, 0), text, font=font)#fill=(255, 0, 0))
    plt.imshow(img)
    plt.show()



def main():
    img= np.array(Image.open('IMG_7259.JPG'))
    ax=image_process2(img)
    Image.fromarray(ax).show()
    #plt.show()
    video_process(video='BANB4867.MP4',output='char.mp4')

if __name__=='__main__':
    main()