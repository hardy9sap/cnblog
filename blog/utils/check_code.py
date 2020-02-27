from PIL import Image, ImageDraw, ImageFont
import random
import string
import io
# 方式一：了解即可
# with open(file='./static/blog/img/login_dir/check_code.png', mode='rb') as fp_img:
#     img_data = fp_img.read()
# return HttpResponse(content=img_data)

# 方式二：
# 磁盘操作太慢
# def get_rgb():
#     r = random.randint(0, 255)
#     g = random.randint(0, 255)
#     b = random.randint(0, 255)
#
#     return r, g, b
#
# img = Image.new(mode='RGB', size=(180, 46), color=get_rgb())  # color='red' / '#000' / (255, 0, 0)
# with open(file='./static/blog/img/login_dir/check_code.png', mode='wb') as fp_img_1:
#     img.save(fp=fp_img_1, format='png')
# with open(file=fp_img_1.name, mode='rb') as fp_img_2:
#     return HttpResponse(content=fp_img_2.read())

# 方式三：
# 将图片写入内存
# fp = io.BytesIO()
#
# def get_rgb():
#     r = random.randint(0, 255)
#     g = random.randint(0, 255)
#     b = random.randint(0, 255)
#     return r, g, b
#
# img = Image.new(mode='RGB', size=(180, 46), color=get_rgb())
# img.save(fp=fp, format='png')
# return HttpResponse(content=fp.getvalue())

# 方式四：
# 加入文字


def get_rgb():
    """
    获取颜色三原色rgb数值
    :return:
    """
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return r, g, b


def get_check_code(request):
    """
    获取验证码
    :param request:
    :return:
    """
    # 获取尺寸
    img_width = int(request.GET.get('width'))
    img_height = int(request.GET.get('height'))

    # 生成图片以及文字
    img = Image.new(mode='RGB', size=(img_width, img_height), color=get_rgb())
    draw = ImageDraw.Draw(im=img)
    font = ImageFont.truetype(font='./static/blog/font/FZZH-FLYYJW.TTF', size=40)
    # 为了实验方便，暂时注释这一段
    cur_check_code = str()  # 保存验证码
    cur_check_code = '123'
    # for count in range(0, 5):
    #     char_type = random.choice([string.ascii_lowercase, string.ascii_uppercase, string.digits])
    #     char = random.choice(list(char_type))
    #     cur_check_code += char
    #     draw.text(xy=(count * 30 + 20, 5), text=char, fill=get_rgb(), font=font)
    request.session['cur_check_code'] = cur_check_code  # 验证码跟用户走

    # 生成验证码图片的噪点噪线（防止机器操作）
    width = img_width
    height = img_height
    for i in range(5):  # 生成噪线
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw.line(xy=(x1, y1, x2, y2), fill=get_rgb())
    #
    for i in range(50):  # 生成噪点
        draw.point(xy=(random.randint(0, width), random.randint(0, height)), fill=get_rgb())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc(xy=(x, y, x + 4, y + 4), start=0, end=90, fill=get_rgb())
    # 写入文件并且返回
    fp = io.BytesIO()
    draw.text(xy=(50, 5), text='123', fill='black')
    img.save(fp=fp, format='png')
    return fp.getvalue()
