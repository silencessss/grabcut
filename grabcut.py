from matplotlib.pyplot import draw
import numpy as np
import cv2

# 定義鼠標事件的回調函數
def on_mouse(event, x, y, flag, param):
    global rect
    global leftButtonDowm
    global leftButtonUp

    # 鼠標左鍵按下
    if event == cv2.EVENT_LBUTTONDOWN:
        rect[0] = x
        rect[2] = x
        rect[1] = y
        rect[3] = y
        leftButtonDowm = True
        leftButtonUp = False

    # 移動鼠標事件
    if event == cv2.EVENT_MOUSEMOVE:
        if leftButtonDowm and not leftButtonUp:
            rect[2] = x
            rect[3] = y

    # 鼠標左鍵松開
    if event == cv2.EVENT_LBUTTONUP:
        if leftButtonDowm and not leftButtonUp:
            x_min = min(rect[0], rect[2])
            y_min = min(rect[1], rect[3])

            x_max = max(rect[0], rect[2])
            y_max = max(rect[1], rect[3])

            rect[0] = x_min
            rect[1] = y_min
            rect[2] = x_max
            rect[3] = y_max
            leftButtonDowm = False
            leftButtonUp = True

# 設定圖像名稱和路徑
image_path = ''
img = cv2.imread(image_path)
img = cv2.resize(img, (540, 960))

# 創建遮罩
mask = np.zeros(img.shape[:2], np.uint8)

# 背景模型和前景模型
bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)
rect = [0, 0, 0, 0]  # 設定需要分割的圖像範圍

leftButtonDowm = False  # 鼠標左鍵按下
leftButtonUp = True  # 鼠標左鍵松開

# 創建窗口並設定鼠標事件回調函數
cv2.namedWindow('img')
cv2.setMouseCallback('img', on_mouse)
cv2.imshow('img', img)

while cv2.waitKey(2) == -1:
    check = 0

    # 左鍵按下，繪製矩形
    if leftButtonDowm and not leftButtonUp:
        img_copy = img.copy()
        cv2.rectangle(img_copy, (rect[0], rect[1]), (rect[2], rect[3]), (0, 255, 0), 2)
        cv2.imshow('img', img_copy)

    # 左鍵松開，矩形畫好
    elif not leftButtonDowm and leftButtonUp and rect[2] - rect[0] != 0 and rect[3] - rect[1] != 0:
        rect[2] = rect[2] - rect[0]
        rect[3] = rect[3] - rect[1]
        rect_copy = tuple(rect.copy())
        rect = [0, 0, 0, 0]

        # 物體分割
        cv2.grabCut(img, mask, rect_copy, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        img_show = img * mask2[:, :, np.newaxis]
        print('[INFO] processing done!')

        # 保存分割結果
        import time
        time_now = time.localtime(time.time())
        time_save = str(time_now[0]) + '_' + str(time_now[1]) + '_' + str(time_now[2]) + '_' + str(time_now[3]) + '_' + str(time_now[4])
        path_save = ''
        cv2.imwrite(path_save, img_show)
        print('[INFO] save done: ' + str(img_name))
        break

cv2.waitKey(0)
cv2.destroyAllWindows()
