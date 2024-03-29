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
"""
pip install opencv-python
"""
import cv2

path = r"./ytest/540.png" # 不可以是中文路径
src = cv2.imread(path, cv2.IMREAD_UNCHANGED)

#percent by which the image is resized
scale_percent = 50

#calculate the 50 percent of original dimensions
width = int(src.shape[1] * scale_percent / 100)
height = int(src.shape[0] * scale_percent / 100)

# dsize
dsize = (width, height)
# resize image
output = cv2.resize(src, dsize)
cv2.imwrite('D:/火车浏览器/cv2-resize-image-50.png',output) 


import cv2

src = cv2.imread('D:/cv2-resize-image-original.png', cv2.IMREAD_UNCHANGED)

# set a new width in pixels
new_width = 300
# dsize
dsize = (new_width, src.shape[0])
# resize image
output = cv2.resize(src, dsize, interpolation = cv2.INTER_AREA)
cv2.imwrite('D:/cv2-resize-image-width.png',output) 


import cv2
 
src = cv2.imread('D:/cv2-resize-image-original.png', cv2.IMREAD_UNCHANGED)

# set a new height in pixels
new_height = 200

# dsize
dsize = (src.shape[1], new_height)
# resize image
output = cv2.resize(src, dsize, interpolation = cv2.INTER_AREA)
cv2.imwrite('D:/cv2-resize-image-height.png',output) 


# 缩放图片
def reduce_img(img_path,need_width=400,savePath='./'):
	filesize = len(open(img_path,'rb').read())/1024
	print(filesize)
	image = cv2.imread(img_path)
	w,h,deep = image.shape
	print(w,h)
	if w > need_width:
		value = rate = math.ceil((need_width / w) * 10) / 10
		resize_img = cv2.resize(image, (0, 0), fx=value, fy=value, interpolation=cv2.INTER_NEAREST)
		basename = os.path.splitext(os.path.split(img_path)[1])[0]
		cv2.imwrite(f'{savePath}{basename}_new.jpg', resize_img)

reduce_img('./zhizhao.jpg')
