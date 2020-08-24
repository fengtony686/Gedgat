from PIL import Image, ImageDraw, ImageFont, ImageFilter
im = Image.open('清华.png')  # 选择打开的图片


def divideColor(im):
     image = Image.new('RGBA', (im.size[0], im.size[1]), (255, 255, 255,1))
     draw = ImageDraw.Draw(image)
     for i in range(im.size[0]):
         for j in range(im.size[1]):
             now_color = im.getpixel((i,j))
             m = bool(i<150 or j<150)  # 边框位置的处理
             n = bool(i>2300 or j>2300)  # 边框位置的处理，这里的图片长宽都是2560 
             k = bool(m or n)
             if now_color[0] >= 255 and k:  # 这里的255根据图片状况选择，指的是去掉红色较浅的部分
                 draw.point((i, j), fill=(255,255,255,0))
             else:
                 draw.point((i, j), fill=now_color)
     image.save('code1.png', 'png')  # code1是图片名称


if __name__ == '__main__':
     divideColor(im)

                 
