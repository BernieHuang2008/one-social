"""
From https://www.cnblogs.com/enumx/p/12359863.html
"""

from PIL import Image
import win32clipboard
import win32con
import io


def copy_img(fname):
    """
    作者：Golden Jet
    链接：https://www.zhihu.com/question/591606899/answer/2952089926
    来源：知乎
    著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
    """
    img = Image.open(fname)  # 输入图片地址
    alpha = img.split()[-1]  # 获取透明通道信息
    # 创建位图对象
    bmp = Image.new('RGBA', img.size, (255, 255, 255, 0))
    bmp.paste(img, mask=alpha)
    # 将位图对象复制到剪切板中
    output = io.BytesIO()
    bmp.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_DIB, data)
    win32clipboard.CloseClipboard()
