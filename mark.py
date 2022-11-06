import cv2

global i
global coordinates


def on_event(event, x, y, flags, img):
    global i
    global coordinates
    if i < 4:
        if event == cv2.EVENT_LBUTTONDOWN:
            xy = "%d,%d" % (x, y)
            coordinates[i][0] = int(x)
            coordinates[i][1] = int(y)
            cv2.circle(img, (x, y), 1, (255, 0, 0), thickness=-1)
            cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                        1.0, (255, 255, 255), thickness=1)
            cv2.imshow("image", img)
            i = i + 1

            print("Now we get No." + str(i) + " point")
    else:
        cv2.destroyWindow("image")


def mark():
    global coordinates
    global i
    i = 0
    coordinates = [[0, 0], [0, 0], [0, 0], [0, 0]]
    print("Now we'll help you get coordinates of pages number in your raw photo")
    raw_photo = input("Please enter your raw photo's path(include *.jpg):")
    img = cv2.imread(raw_photo)
    cv2.namedWindow("image", cv2.WINDOW_KEEPRATIO)
    cv2.setMouseCallback("image", on_event, img)
    cv2.imshow("image", img)
    while i < 4:
        cv2.waitKey(20)
    cv2.destroyWindow("image")
    # print(coordinates)
    # print(type(coordinates))
    return coordinates

