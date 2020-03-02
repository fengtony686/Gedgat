from PIL import Image, ImageDraw, ImageFont


SAVE_PATH = "D://save.jpeg"  # 存储地址
FONT_SIZE = 8  # 插入的字体大小
TEXT = "I love you!"  # 需要输入的文字
IMG_PATH = "./img.jpg"  # 图片地址
FONT_PATH = 'C:/Windows/fonts/Arial.ttf'  # 字体文件地址


img_raw = Image.open(IMG_PATH)
img_array = img_raw.load()
img_new = Image.new("RGB", img_raw.size, (0, 0, 0))
draw = ImageDraw.Draw(img_new)
font = ImageFont.truetype(FONT_PATH, FONT_SIZE)


def character_generator(text):
    while True:
        for i in range(len(text)):
            yield text[i]


ch_gen = character_generator(TEXT)


for y in range(0, img_raw.size[1], font_size):
    for x in range(0, img_raw.size[0], font_size):
        draw.text((x, y), next(ch_gen), font=font, fill=img_array[x, y], direction=None)


img_new.convert('RGB').save("SAVE_PATH")
