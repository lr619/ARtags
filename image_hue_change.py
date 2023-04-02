import cv2

original_image = cv2.imread(r"C:\Users\Pjixels\documents\Coding\HackpsuSpring2023\images\ColorCard.jpg")
#altered_image = cv2.imread("")


original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)
altered_image = cv2.cvtColor(altered_image, cv2.COLOR_BGR2HSV)


def average_saturation_subimage_overall(image):
    subimage = image[:, :, 1]
    return subimage.mean()

def average_brightness_subimage_overall(image):
    subimage = image[:, :, 2]
    return subimage.mean()

def imgBlender(image, ogColor, newColor):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    image = cv2.resize(image, (640, 800))

    saturation_increment = average_saturation_subimage_overall(newColor)-average_saturation_subimage_overall(ogColor)
    brightness_increment = average_brightness_subimage_overall(newColor)-average_brightness_subimage_overall(ogColor)

    image[:,:,1] = cv2.add(image[:, :, 2], saturation_increment)
    image[:,:,2] = cv2.add(image[:, :, 1], brightness_increment)
    image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
    return image;