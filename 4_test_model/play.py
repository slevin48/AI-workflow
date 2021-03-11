# play.py
from utils import resize_image, Sample
# from termcolor import cprint

# from train.py
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D
from keras import optimizers
from keras import backend as K

# from test_model.py
import numpy as np
from grabscreen import grab_screen
import cv2
import time
from directkeys import PressKey,ReleaseKey, Z, Q, S, D
from getkeys import key_check

import random


MODEL_NAME = 'model_weights.h5'


# Global variable
OUT_SHAPE = 5
INPUT_SHAPE = (Sample.IMG_H, Sample.IMG_W, Sample.IMG_D)


def create_model(keep_prob = 0.8):
    model = Sequential()

    # NVIDIA's model
    model.add(Conv2D(24, kernel_size=(5, 5), strides=(2, 2), activation='relu', input_shape= INPUT_SHAPE))
    model.add(Conv2D(36, kernel_size=(5, 5), strides=(2, 2), activation='relu'))
    model.add(Conv2D(48, kernel_size=(5, 5), strides=(2, 2), activation='relu'))
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
    model.add(Flatten())
    model.add(Dense(1164, activation='relu'))
    drop_out = 1 - keep_prob
    model.add(Dropout(drop_out))
    model.add(Dense(100, activation='relu'))
    model.add(Dropout(drop_out))
    model.add(Dense(50, activation='relu'))
    model.add(Dropout(drop_out))
    model.add(Dense(10, activation='relu'))
    model.add(Dropout(drop_out))
    model.add(Dense(OUT_SHAPE, activation='softsign'))

    return model


t_time = 0.09

def straight():
##    if random.randrange(4) == 2:
##        ReleaseKey(Z)
##    else:
    PressKey(Z)
    ReleaseKey(Q)
    ReleaseKey(D)

def left():
    # PressKey(Z)
    PressKey(Q)
    #ReleaseKey(Z)
    ReleaseKey(D)
    #ReleaseKey(Q)
    time.sleep(t_time)
    ReleaseKey(Q)

def right():
    # PressKey(Z)
    PressKey(D)
    ReleaseKey(Q)
    #ReleaseKey(Z)
    #ReleaseKey(D)
    time.sleep(t_time)
    ReleaseKey(D)


# Play
class Actor(object):

    def __init__(self):
        # Load in model from train.py and load in the trained weights
        self.model = create_model(keep_prob=1) # no dropout
        self.model.load_weights(MODEL_NAME)


    def get_action(self, obs):

        ## Look
        vec = resize_image(obs)
        vec = np.expand_dims(vec, axis=0) # expand dimensions for predict, it wants (1,66,200,3) not (66, 200, 3)
        ## Think
        joystick = self.model.predict(vec, batch_size=1)[0]

        ## Act
        ### calibration
        output = [
            joystick[0],
            joystick[1],
            joystick[2],
            joystick[3],
            joystick[4],
        ]

        # print("AI: " + str(output))

        return joystick


if __name__ == '__main__':
    last_time = time.time()
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)

    paused = False
    while(True):
        
        if not paused:
            # 800x600 windowed mode
            #screen =  np.array(ImageGrab.grab(bbox=(0,40,800,640)))
            screen = grab_screen(region=(0,40,960,560))
            print('loop took {} seconds'.format(time.time()-last_time))
            last_time = time.time()

            actor = Actor()

            prediction = actor.get_action(screen)
            print(prediction)

            turn_thresh = 0.50
            fwd_thresh = 0.75

            if prediction[0] > turn_thresh:
                right()
                # print("right")
            elif prediction[0] < -turn_thresh:
                left()
                # print("left")
            elif prediction[2] > fwd_thresh:
                straight()
                # print("straight")
            # elif prediction[2] < fwd_thresh:
            #     print("NOKEY")
            else:
                straight()

        keys = key_check()
        print(keys)

        # p pauses game
        if 'T' in keys:
            if paused:
                paused = False
                time.sleep(1)
            else:
                paused = True
                ReleaseKey(Q)
                ReleaseKey(Z)
                ReleaseKey(D)
                time.sleep(1)
        
        # b breaks the loop
        if 'B' in keys:
            break