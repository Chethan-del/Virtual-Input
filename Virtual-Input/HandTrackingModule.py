import cv2
import mediapipe as mp

class handDetector():
    def __init__(self, mode = False, maxHands = 2, modelComplexity = 1, detectionCon = 0.7, trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands # formality

        #intialize a mediapipe handobject
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex, self.detectionCon, self.trackCon) #hand detection
        self.mpDraw = mp.solutions.drawing_utils # object to draw hand landmarks
        self.tipIds = [4, 8, 12, 16, 20]

#landmarks is a ratio of img

    def findHands(self, img, draw = True): # draw False removes the landmarks and connections in image
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB) #process and returns landmarks as output
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS) # mpHands.HAND_CONNECTIONS to draw connections
        return img

    #function for converting ratio landmarks to pixel values landmarks
    def findPosition(self, img, handNo = 0, draw = True): # draw False removes the highlighted landmarks in image
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape  # fetching height, width, channel from the image
                cx, cy = int(lm.x*w), int(lm.y*h)  # converting the landmark ratios in terms of pixel position
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx,cy), 5, (255,0,0),cv2.FILLED)
        return self.lmList


#This condition compares the x-coordinate of the tip of the thumb (landmark at self.tipIds[0]) with the x-coordinate
# of the base of the thumb (landmark at self.tipIds[0]-1). If the tip is to the left
# of the base (lower x-coordinate), it means the thumb is up
    def fingersUp(self):
        fingers = []
        #thumb

        if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

            # remaining fingers
        for id in range(1,5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers


'''[landmark {
  x: 0.6466354727745056
  y: 0.9883676767349243
  z: 2.76076036698214e-07
}
landmark {
  x: 0.601280927658081
  y: 0.9832119941711426
  z: -0.018430497497320175
}
]'''