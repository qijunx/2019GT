# -*-coding:utf-8-*-
# 导入所需要的模块
from PIL import Image
from urllib import request
from aip import AipOcr


# 读取图片
def get_file_content(image):
    with open(image, 'rb') as fp:
        return fp.read()


# 对图片进行一系列的处理，便于后期OCR识别
def picture_processing(image):
    # 使图像变成灰度图像
    image = image.convert('L')
    # image.show()
    # 对图像进行二值化处理
    threshold = 127  # 设置的阈值
    table = []
    for i in range(256):
        # 如果像素偏白
        if i < threshold:
            # 去除偏白的像素
            table.append(0)
        # 像素偏黑
        else:
            # 保留偏黑的像素
            table.append(1)
    # 按像素信息绘制
    image = image.point(table, '1')
    # 保存
    image.save("captcha1.jpg")


# OCR识别
def ocr_distinguish(url):
    # 百度AI上创建的文字识别应用
    # 以下是我创建的应用对应于我的应用信息，不可外传
    app_id = "16949803"
    api_key = "LwOgZ3kzNtGobdXjU8gMuyGp"
    secret_key = "O5nMZeGrrfxj1kFUvLyyeGTBKiG6Tycy"

    aipocr = AipOcr(app_id, api_key, secret_key)
    # 从url获取图片，并将图片下载到本地
    request.urlretrieve(url, "captcha1.jpg")
    image = Image.open("captcha1.jpg")
    # 图片处理
    picture_processing(image)
    image.show()
    options = {
        'detect_direction': 'true',
        'language_type': 'CHN_ENG',
    }

    image = get_file_content("captcha1.jpg")

    results = aipocr.basicGeneral(image, options)

    try:
        code = results['words_result'][0]['words']
    except:
        code = '验证码匹配失败'

    print(code.replace(" ", ""))
    return code.replace(" ", "")


if __name__ == '__main__':
    v_yzm_url = "http://jw.hpu.edu.cn/validateCodeAction.do"  # 验证码图片的url

    v_yzm = ocr_distinguish(v_yzm_url)
