import os
import cv2
import numpy as np
import pandas as pd
import tensorflow as tf

from datetime import datetime


"Class manage all the model mission"


class Model:

    # image_list, steering_list

    count = 0
    count_folder = 0

    def __init__(self):

        self.label = ""

        self.width = 48
        self.height = 48

        self.image_list = []
        self.steering_list = []

        self.collecting_status = False

        self.my_dir, self.new_path = "", ""

        self.model = tf.keras.models.load_model("Traffic Models/Model_Traffic_Sign.h5", compile=False)

        self.labels = ["Speed limit (20km/h)", "Speed limit (30km/h)",
                       "Speed limit (50km/h)", "Speed limit (60km/h)", "Speed limit (70km/h)",
                       "Speed limit (80km/h)", "End of speed limit (80km/h)",
                       "Speed limit (100km/h)", "Speed limit (120km/h)", "No passing",
                       "No passing for vehicles over 3.5 metric tons",
                       "Right-of-way at the next intersection",
                       "Priority road", "Yield", "Stop", "No vehicles",
                       "Vehicles over 3.5 metric tons prohibited", "No entry",
                       "General caution", "Dangerous curve to the left",
                       "Dangerous curve to the right", "Double curve", "Bumpy road",
                       "Slippery road", "Road narrows on the right", "Road work",
                       "Traffic signals", "Pedestrians", "Children crossing",
                       "Bicycles crossing", "Beware of ice/snow", "Wild animals crossing",
                       "End of all speed and passing limits", "Turn right ahead",
                       "Turn left ahead", "Ahead only", "Go straight or right",
                       "Go straight or left", "Keep right", "Keep left", "Roundabout mandatory",
                       "End of no passing", "End of no passing by vehicles over 3.5 metric"]

    def get_label(self):
        return self.label

    # Collect data before training
    def collect_data(self, frame, steering):

        if not self.collecting_status:
            self.collecting_status = True
            self.my_dir, self.new_path = Model.define_path()
        else:
            # Save frame in folder
            Model.save_data(self, frame, steering)

    @staticmethod
    # Method define path to save data collection
    def define_path():

        # Get current directory path
        my_dir = os.path.join(os.getcwd(), 'DataCollected')

        # Create new folder base on the previous folder
        while os.path.exists(os.path.join(my_dir, f'IMG{str(Model.count_folder)}')):
            Model.count_folder += 1

        new_path = my_dir + "/IMG" + str(Model.count_folder)
        os.makedirs(new_path)

        return my_dir, new_path

    # Function save frame in folder
    def save_data(self, img, steering):

        # global image_list, steering_list

        now = datetime.now()
        timestamp = str(datetime.timestamp(now)).replace('.', '')

        file_name = os.path.join(self.new_path, f'Image_{timestamp}.jpg')
        cv2.imwrite(file_name, img)

        self.image_list.append(file_name)
        self.steering_list.append(steering)

    # Save log file when the session end
    def save_log(self):

        self.collecting_status = False

        raw_data = {'Image': self.image_list, 'Steering': self.steering_list}

        df = pd.DataFrame(raw_data)
        df.to_csv(os.path.join(self.my_dir, f'log_{str(Model.count_folder)}.csv'), index=False, header=False)

    # Method predict label from the model
    def predict(self, img):

        # Fit the model size to model input
        img = Model.preprocess(self, img)

        # Store the model prediction scores
        scores = self.model.predict(img)

        # Store the high label score
        self.label = self.labels[np.argmax(scores)]

        return self.label

    # Method reshape image before model prediction
    def preprocess(self, img):

        # Resizing frame to the right shape of the model's input
        if img.shape[0] != self.height or img.shape[1] != self.width:
            img = cv2.resize(img, (self.width, self.height), interpolation=cv2.INTER_CUBIC)

        # Extending dimension from (height, width, channels) to (1, height, width, channels)
        img = img[np.newaxis, :, :, :]

        return img
