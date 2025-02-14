import cv2
from blend_images import blend_images

if __name__ == '__main__':
    watermark = cv2.imread("res/img/youtube.png")
    src = cv2.imread("res/img/windows-background.png")

    ratio = 0.2
    x_offset = 100
    y_offset = 100

    result = blend_images(src, watermark, (y_offset, x_offset), 0.5, 0.2)

    cv2.imshow("result", result)
    cv2.waitKey(0)
