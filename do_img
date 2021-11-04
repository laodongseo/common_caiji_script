改变图片尺寸：

from PIL import Image

basewidth = 300
img = Image.open('fullsized_image.jpg')
wpercent = (basewidth / float(img.size[0]))
hsize = int((float(img.size[1]) * float(wpercent)))
img = img.resize((basewidth, hsize), Image.ANTIALIAS)
img.save('resized_image.jpg')


from PIL import Image

baseheight = 560
img = Image.open('fullsized_image.jpg')
hpercent = (baseheight / float(img.size[1]))
wsize = int((float(img.size[0]) * float(hpercent)))
img = img.resize((wsize, baseheight), Image.ANTIALIAS)
img.save('resized_image.jpg')
------------------------------------------------------------------------------
