#coding=utf-8
from random import randint, choice
from PIL import Image, ImageDraw, ImageFont
from cStringIO import StringIO
from string import printable

def create_captcha():
    font_path = "utils/captcha/font/Arial.ttf"
    font_color = (randint(150,200), randint(0,150), randint(0,150))
    line_color = (randint(0,150), randint(0,150), randint(150,200))
    point_color = (randint(0, 150), randint(50, 150), randint(150, 200))
    width, height = 100, 40
    image = Image.new('RGB', (width, height), (200, 200, 200))
    font = ImageFont.truetype(font_path, height-10)
    draw = ImageDraw.Draw(image)
    #生成验证码
    print printable
    text =''.join([choice(printable[:62]) for i in xrange(4)])
    font_width, font_height = font.getsize(text)
    #把验证码写到画布上
    draw.text((10,10), text, font=font, fill=font_color)
    #绘制线条
    for i in xrange(0, 5):
        draw.line(((randint(0, width), randint(0, height)),
                   (randint(0, width), randint(0, height))),
                  fill=line_color, width=2)
    #绘制点
    for i in xrange(randint(100, 1000)):
        draw.point((randint(0, width), randint(0, height)), fill=point_color)
    #输出
    out = StringIO()
    image.save(out, format='jpeg')
    content = out.getvalue()
    out.close()
    print '图型验证码',text
    return text, content


    # font_path = "utils/captcha/font/Arial.ttf"
    # #img 是画板
    # img = Image.open('/home/pyvip/tornado_test_002/utils/captcha/image5.jpg')
    # #draw是画笔
    # draw = ImageDraw.Draw(img)
    # draw.line(((0,0), (100,100)), fill=(255, 0,0), width=5 )
    # font = ImageFont.truetype(font_path, 200)
    # draw.text((100,100), 'BCD', font= font, fill=(0,255,0))
    # width = 500
    # height = 500
    # for i in xrange(0, 5):
    #     draw.line(((randint(0, width), randint(0, height)),
    #                (randint(0, width), randint(0, height))),
    #               fill=(0,0,255), width=2)
    #
    # for i in xrange(randint(10000, 100000)):
    #     draw.point((randint(0, width), randint(0, height)), fill=(255,50,50))
    #
    # out = StringIO()
    # print dir(out)
    # img.save(out, format='jpeg')
    # content = out.getvalue()
    # out.close()
    # text ='aaa'
    # print '图型验证码',text
    # return text, content









