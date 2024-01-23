from detect import food_detection
import cv2


im0s = cv2.imread('test_image.jpg')  # BGR
result, label, total_calorie = food_detection(im0s)
print("음식 :",label)
print("총 칼로리 :", total_calorie)
cv2.imwrite("result.png", result)