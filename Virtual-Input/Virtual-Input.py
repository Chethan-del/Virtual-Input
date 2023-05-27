import HandTrackingModule as htm
from tensorflow.keras.models import load_model
import WindowController as Win
import cv2
import numpy as np
import keyboard
import pygame
import time
import os

wc = Win.WindowControl()

buttonPressed = False
buttonCounter = 0
buttonDelay = 25


def gesture_recognize(landmarks, modeValue):
    global buttonPressed

    if modeValue == "Win_control":
        labels = ['','Close', '', 'Resize', 'Open', 'Toggle', 'Maximize', '', '', '']
        model = load_model('model.h5')
    elif modeValue == "Emoji":
        labels = ['Super','peace','thumbs up','thumbs down','call me','stop','rock','live long','fist', 'Smile']
        model = load_model('model.h5')


        # call me - open
        # rock - maximize
        # thumbdown - resize
        # stop - toggle windows
        # peace - close window



    # If landmarks are found, prepare the image for the CNN model
    if len(landmarks) > 0 and buttonPressed is False:
        # Reshape the image into a (1, 21, 2) array
        image = np.array(landmarks)[:21, 1:]
        image = image.reshape((1, 21, 2))

        # Use the CNN model to predict the class of the hand gesture
        prediction = model.predict(image)
        class_index = np.argmax(prediction)
        class_label = labels[class_index]
        buttonPressed = True
        return class_label

def strt():
    global buttonPressed, buttonCounter, buttonDelay

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (0, 0, 255)
    YELLOW = (0, 255, 255)
    GREEN = (0, 255, 0)
    BACKGROUND = (255, 255, 255)
    FORGROUND = (0, 255, 0)
    BORDER = (0, 255, 0)
    last_color = (0, 0, 1)
    draw_color = (0, 0, 255)
    BOUNDRYINC = 5

    #CV2 
    cap = cv2.VideoCapture(0)
    width, height = 1280, 720
    cap.set(3, width)  # 640, 1280
    cap.set(4, height)  # 480, 720
    imageCanvas = np.zeros((height, width, 3), np.uint8)

    pygame.init()
    WINDOW = pygame.display.set_mode((width, height), flags=pygame.HIDDEN)
    pygame.display.set_caption("Digit Board")
    x_coordinate = []
    y_coordinate = []

    #Header
    folderPath = "header"
    myList = os.listdir(folderPath)
    overlayList = []

    for imPath in myList:
        image = cv2.imread(f'{folderPath}/{imPath}')
        overlayList.append(image)
    header = overlayList[0]

    #model
    label = ""
    OUTPUT = "off"
    AlphaMODEL = load_model("Alpha_Model.h5")
    NumMODEL = load_model("num_model.h5")

    alpha_bet = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j',
                   10: 'k', 11: 'l', 12: 'm', 13: 'n', 14: 'o', 15: 'p', 16: 'q', 17: 'r', 18: 's', 19: 't',
                   20: 'u', 21: 'v', 22: 'w', 23: 'x', 24: 'y', 25: 'z', 26: ''}
    num_ber = {0: '0', 1: '1', 2: '2',
                 3: '3', 4: '4', 5: '5',
                 6: '6', 7: '7', 8: '8',
                 9: '9'}

    detector = htm.handDetector(detectionCon=0.8)
    xp, yp = 0, 0
    brush_thickness = 15
    modeValue = "OFF"
    modeColor = RED

    while True:
        SUCCESS, image = cap.read()
        image = cv2.flip(image, 1)

        image = detector.findHands(image)
        landmarks = detector.findPosition(image, draw=False)
        cv2.putText(image, "Press A for Alphabate Recognisition Mode ", (0, 145), 3, 0.5, (255, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(image, "Press N for Digit Recognisition Mode ", (0, 162), 3, 0.5, (255, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(image, "Press E for Emoji Recognition Mode ", (0, 179), 3, 0.5, (255, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(image, "Press W for Window Control mode ", (0, 196), 3, 0.5, (255, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(image, "Press O for Turn Off Recognisition Mode ", (0, 213), 3, 0.5, (255, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(image, "Press Q for Quitting The Window", (0, 230), 3, 0.5, (255, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(image, f'{"RECOGNISITION IS "}{modeValue}', (0, 247), 3, 0.5, modeColor, 1, cv2.LINE_AA)
        #cv2.putText(image, text, org, fontFace, fontScale, color, thickness, lineType)

        #Keyboard selection
        if keyboard.is_pressed('a'):
            if OUTPUT != "alpha":
                OUTPUT = "alpha"
                modeValue, modeColor = "ALPHABATES", GREEN

        if keyboard.is_pressed('n'):
            if OUTPUT != "num":
                OUTPUT = "num"
                modeValue, modeColor = "NUMBER", YELLOW

        if keyboard.is_pressed('o'):
            if OUTPUT != "off":
                OUTPUT = "off"
                modeValue, modeColor = "OFF", YELLOW

        if keyboard.is_pressed('e'):
            if OUTPUT != "emoji":
                OUTPUT = "emoji"
                modeValue, modeColor = "Emoji", YELLOW

        if keyboard.is_pressed('w'):
            if OUTPUT != "win_control":
                OUTPUT = "win_control"
                modeValue, modeColor = "Win_control", YELLOW

        if keyboard.is_pressed('q'):
            cap.release()
            cv2.destroyAllWindows()
            quit()

            xp, yp = 0, 0
            label = ""
            x_coordinate = []
            y_coordinate = []
            time.sleep(0.5)

        #Window control Operations
        if OUTPUT == 'win_control':
            con_label = gesture_recognize(landmarks, modeValue)
            buttonPressed = True
            class_label = str(con_label)

            # Draw the predicted label on the image
            cv2.putText(image, class_label, (1000, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            if con_label == 'Resize':
                time.sleep(1)
                wc.resize_window()
                time.sleep(1)
            elif con_label == 'Maximize':
                time.sleep(1)
                wc.maximize_window()
                time.sleep(1)
            elif con_label == 'Close':
                time.sleep(1)
                wc.close_window()
                time.sleep(1)
            elif con_label == 'Toggle':
                time.sleep(1)
                wc.toggle_window()
                time.sleep(1)
            elif con_label == 'Open':
                time.sleep(1)
                wc.open_window()
                time.sleep(1)

        #Emoji recognition
        if OUTPUT == 'emoji':
                label_str = gesture_recognize(landmarks, modeValue)
                buttonPressed = True
                class_label = str(label_str)
                emoji = {'okay': '👌', 'peace' : '✌',  'thumbs up' : '👍', 'thumbs down' : '👎', 'call me' :'🤙' , 'stop' : '✋', 'rock' : '🤘', 'live long' : '🖖',  'fist' : '✊', 'smile' : '😊'}
                if class_label != 'None':
                    fh = open('Output.txt', 'a', encoding='utf-8')
                    fh.write(emoji[class_label])
                    fh.close()
                # Draw the OUTPUTed label on the image
                cv2.putText(image, class_label, (1000, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    


        if buttonPressed:
            buttonCounter += 1
            if buttonCounter > buttonDelay:
                buttonCounter = 0
                buttonPressed = False

        #character recognition
        if OUTPUT == 'alpha' or OUTPUT == 'num':
            if len(landmarks) > 0:

                x1, y1 = landmarks[8][1:]
                x2, y2 = landmarks[12][1:]

                fingers = detector.fingersUp()

                #This part of the code checks for 2 finger selection
                if fingers[1] and fingers[2]:

                    # add

                    x_coordinate = sorted(x_coordinate)
                    y_coordinate = sorted(y_coordinate)

                    #Based on the coordinates it draws the bounding box
                    if (len(x_coordinate) > 0 and len(y_coordinate) > 0 and OUTPUT != "off"):
                        if draw_color != (0, 0, 0) and last_color != (0, 0, 0):
                            rect_min_x, rect_max_x = max(x_coordinate[0] - BOUNDRYINC, 0), min(width, x_coordinate[
                                -1] + BOUNDRYINC)
                            rect_min_y, rect_max_y = max(0, y_coordinate[0] - BOUNDRYINC), min(
                                y_coordinate[-1] + BOUNDRYINC, height) #
                            x_coordinate = []
                            y_coordinate = []

                            pygame.PixelArray(WINDOW) #creates a new image of bounding box
                            image_arr = np.array(pygame.PixelArray(WINDOW))[rect_min_x:rect_max_x,
                                      rect_min_y:rect_max_y].T.astype(np.float32)

                            #draws the box on the screen
                            cv2.rectangle(imageCanvas, (rect_min_x, rect_min_y), (rect_max_x, rect_max_y), BORDER, 3)
                            image = cv2.resize(image_arr, (28, 28))

                            image = np.pad(image, (10, 10), 'constant', constant_values=0)
                            image = cv2.resize(image, (28, 28)) / 255


                            if OUTPUT == "alpha":
                                label = str(alpha_bet[np.argmax(AlphaMODEL.OUTPUT(image.reshape(1, 28, 28, 1)))])
                            if OUTPUT == "num":
                                label = str(num_ber[np.argmax(NumMODEL.predict(image.reshape(1, 28, 28, 1)))])
                            pygame.draw.rect(WINDOW, BLACK, (0, 0, width, height))

                            fh = open('Output.txt', 'a')
                            fh.write(label)
                            fh.close()

                            #draws the text above the displayed rectangle
                            cv2.rectangle(imageCanvas, (rect_min_x + 50, rect_min_y - 30), (rect_min_x, rect_min_y),BACKGROUND, -1)
                            #cv2.rectangle(image, pt1, pt2, color, thickness, lineType, shift)

                            cv2.putText(imageCanvas, label, (rect_min_x, rect_min_y - 5), 3, 1, FORGROUND, 1, cv2.LINE_AA)
                           # cv2.putText(image, text, org, fontFace, fontScale, color, thickness, lineType, bottomLeftOrigin)
                        else:

                            # if a text is not drawn
                            x_coordinate = []
                            y_coordinate = []

                    #to select which color canvas
                    xp, yp = 0, 0
                    if y1 < 125:
                        last_color = draw_color
                        if 0 < x1 < 200:
                            imageCanvas = np.zeros((height, width, 3), np.uint8)
                        elif 210 < x1 < 320:
                            header = overlayList[0]
                            draw_color = (0, 0, 255)
                        elif 370 < x1 < 470:
                            header = overlayList[1]
                            draw_color = (0, 255, 255)
                        elif 520 < x1 < 630:
                            header = overlayList[2]
                            draw_color = (0, 255, 0)
                        elif 680 < x1 < 780:
                            header = overlayList[3]
                            draw_color = (255, 0, 0)
                        elif 890 < x1 < 1100:
                            header = overlayList[4]
                            draw_color = (0, 0, 0)
                            imageCanvas = np.zeros((height, width, 3), np.uint8)
                        elif 1160 < x1 < 1250:
                            cap.release()
                            cv2.destroyAllWindows()
                            quit()

                    #draws rectangle on finger tip
                    cv2.rectangle(image, (x1, y1 - 25), (x2, y2 + 25), draw_color, cv2.FILLED)
                    #cv2.rectangle(image, pt1, pt2, color, thickness, lineType,)

                #if only single fingle drawing is enabled
                elif fingers[1] and fingers[2] == False:

                    # add
                    x_coordinate.append(x1)
                    y_coordinate.append(y1)
                    # addEnd

                    cv2.circle(image, (x1, y1 - 15), 15, draw_color, cv2.FILLED)
                    if xp == 0 and yp == 0:
                        xp, yp = x1, y1

                    if draw_color == (0, 0, 0):
                        pass
                    else:
                        cv2.line(image, (xp, yp), (x1, y1), draw_color, brush_thickness)
                        cv2.line(imageCanvas, (xp, yp), (x1, y1), draw_color, brush_thickness)
                        pygame.draw.line(WINDOW, WHITE, (xp, yp), (x1, y1), brush_thickness)
                    xp, yp = x1, y1
                else:
                    xp, yp = 0, 0

            #Normalizing
            imageGray = cv2.cvtColor(imageCanvas, cv2.COLOR_BGR2GRAY)
            _, imageInv = cv2.threshold(imageGray, 50, 255, cv2.THRESH_BINARY_INV)
            imageInv = cv2.cvtColor(imageInv, cv2.COLOR_GRAY2BGR)
            image = cv2.bitwise_and(image, imageInv)
            image = cv2.bitwise_or(image, imageCanvas)

        image[0:132, 0:1280] = header
        pygame.display.update()
        cv2.imshow("Input Window", image)
        cv2.waitKey(1)

strt()