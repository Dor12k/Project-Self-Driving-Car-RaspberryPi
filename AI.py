

import cv2
import threading
import numpy as np

from Model import Model


"Class manage all the Artificial Intelligence functions"


class AI:

    if True:
        curve_list = []
        average_values = 10

        # Define tracker dictionary
        tracker_dict = {'kcf': cv2.TrackerKCF_create,
                        'mil': cv2.TrackerMIL_create,
                        'tld': cv2.TrackerTLD_create,
                        'csrt': cv2.TrackerCSRT_create,
                        'mosse': cv2.TrackerMOSSE_create,
                        'boosting': cv2.TrackerMOSSE_create,
                        'medianflow': cv2.TrackerMedianFlow_create}

    def __init__(self):

        # Variable of Tensorflow model
        self.model = Model()

        # Variable of limited motor speed
        self.max_speed = 80

        # Variable the model prediction status
        self.predicting = False

        # Variable is a flag of detection process
        self.traffic_sign_detected = False

        # Variable hold detection traffic sign status
        self.detecting = False

        # Initialize our tracker after the object
        self.tracker = AI.tracker_dict['kcf']()

        self.traffic_sign = ["", [0, 0, 0, 0]]
        self.traffic_signs = ["Speed limit (30km/h)", "Speed limit (50km/h)", "Pedestrians", "No entry", "Stop"]

    # Method detect traffic sign
    def traffic_sign_detection(self, frame, mask_frame, process, motor):

        # Check if we need to detect or just keep tracking
        if not self.traffic_sign_detected:

            # Crop the suspected zone for track sign
            roi_frame = frame[:frame.shape[0]//2, frame.shape[1]//2:]

            # Function return mask edge frame and bounding box boundaries area
            edge_frame, min_area, max_area = process.canny_edge_detection(roi_frame)

            # Detect traffic sign and bounding box coordinates
            AI.traffic_sign_detector(self, frame, edge_frame, roi_frame, min_area, max_area)
        else:
            # Get the bounding box from the frame
            (success, contour_box) = self.tracker.update(frame)

            if success:
                AI.update_traffic_sign(self, frame, contour_box)
            else:
                AI.initialize_traffic_sign(self)

    # Method initialize traffic sign label and coordinates
    def initialize_traffic_sign(self):
        self.traffic_sign_detected = False
        self.traffic_sign = ["", [0, 0, 0, 0]]

    # Method update traffic sign label and coordinates
    def update_traffic_sign(self, frame, contour_box):

        # Change coordinates to int
        x, y, w, h = [int(coordinate) for coordinate in contour_box]

        # Function check if bounding box is in frame boundaries
        in_boundaries = AI.check_boundaries(frame, x, y, w, h)

        if not in_boundaries:
            AI.initialize_traffic_sign(self)
        else:
            self.traffic_sign[1] = [x, y, w, h]

    @staticmethod
    # Method check of coordinated inside the frame boundaries
    def check_boundaries(frame, x, y, w, h):

        if frame.shape[1] < x + w or frame.shape[0] < y + h:
            return False
        else:
            return True

    # Method detect traffic sign
    def traffic_sign_detector(self, frame, edge_frame, roi_frame, min_area, max_area):

        if not self.detecting:

            # Update detection status
            self.detecting = True

            # Initialize traffic sign variable
            self.traffic_sign = ["", [0, 0, 0, 0]]

            # Function return array of all contours we found
            _, contours, hierarchy = cv2.findContours(edge_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

            # Sorted the contours and define the larger first
            contours = sorted(contours, key=cv2.contourArea, reverse=True)

            for contour in contours:
                area = cv2.contourArea(contour)
                if area < max_area:
                    if min_area < area:

                        # Function return the suspicious ROI and coordinates
                        fragment, coordinates = AI.cut_fragment(frame, roi_frame, contour)

                        # Function return label prediction from model
                        traffic_sign = AI.traffic_sign_prediction(self, fragment)

                        if traffic_sign in self.traffic_signs:

                            self.detecting = False
                            self.traffic_sign_detected = True

                            # Add the detected object to the tracker
                            self.tracker = self.tracker_dict['csrt']()
                            self.tracker.init(frame, tuple(coordinates))

                            return edge_frame, traffic_sign

            self.detecting = False
            return edge_frame, ""
        else:
            return edge_frame, self.traffic_sign

    @staticmethod
    # Method cut ROI from frame and return coordinates
    def cut_fragment(image, roi, contour):

        # approximate the contour
        peri = cv2.arcLength(contour, True)

        # Contour points
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

        # Length give us the shape of polygon
        corners_num = len(approx)

        crop_x, crop_y, crop_w, crop_h = cv2.boundingRect(approx)

        # Cut the fragment before prediction
        fragment = roi[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]

        x = (image.shape[1] // 2) + crop_x
        y = crop_y  # (frame.shape[0] // 2) + crop_y
        w = crop_w
        h = crop_h

        coordinates = [x, y, w, h]

        return fragment, coordinates

    # Method predict the Roi fragment by the traffic sign model
    def traffic_sign_prediction(self, fragment):

        if self.predicting:
            return self.traffic_sign[0]
        else:
            self.predicting = True

            t = threading.Thread(target=self.model.predict, args=(fragment,), daemon=True)
            t.name = "Prediction"
            t.start()
            t.join()

            label = self.model.get_label()

            self.predicting = False
            self.traffic_sign[0] = label

            return self.traffic_sign[0]

    # Method manage the autonomic drive
    def self_driving(self, frame, mask_frame, process, motor, system, road_type):

        # Reset the traffic sign tracking
        if not system.tracking:
            system.tracking = True
            AI.initialize_traffic_sign(self)

        # Collect data
        if system.collect_data:
            # Save frame in folder
            system.collect_data = AI.collect_data(self, frame, system.turn, system.end_collect_data)

        # Function detect traffic sign on the road
        AI.traffic_sign_detection(self, frame, mask_frame, process, motor)

        # Drawing bounding box around the traffic sign
        AI.bounding_traffic_sign(self, frame, self.traffic_sign[1])

        # Get the traffic sign instruction
        temp_bool, max_speed = AI.traffic_sign_decoder(self, self.traffic_sign, 0)

        # Function return warp image of the curve and frame with drawn points
        frame, warp_image = AI.curve_adjustment(frame, mask_frame, process)

        if road_type == 1:
            pass
            # Draw color on the curve
            # inv_wrap, img_lane, frame = AI.draw_lane(frame, mask)

            # Function return curve direction and if display is true it will draw the lane in green
            curve_direction = AI.curve_direction(frame, mask_frame, process)

            # Draw color on the curve
            inv_wrap, img_lane, frame = AI.draw_lane(frame, mask_frame)

            # Find the right direction according to the lane
            speed, turn, time = AI.aim_car_direction(curve_direction, max_speed)

        else:
            print("Class AI: self-driving function. need to define road type")
            speed, turn, time = 0, 0, 0

        system.speed = speed
        system.turn = turn
        system.time = time

        return frame, warp_image, system

    @staticmethod
    # Method find the curve direction
    def curve_direction(frame, mask_frame, process):

        # Function return middle point and if display is true it will draw the lane in green
        mid_point, histogram_crop = process.get_histogram(frame, mask_frame, display=False, min_percent=0.5, region=4)

        # Function return average point and if display is true it will draw the lane in green
        average_point, histogram_curve = process.get_histogram(frame, mask_frame, display=False, min_percent=0.5, region=1)

        # Define the curve direction value
        curve_direction = mid_point - average_point

        return curve_direction

    @staticmethod
    # Method change the angle perspective of the curve and mark the boundaries
    def curve_adjustment(frame, mask_frame, process):

        # Function return wrap image and points from bar
        warp_image, points = process.get_warp_image(mask_frame)

        # Function draw the points on the frame
        frame = process.draw_points(frame, np.array(points))

        return frame, warp_image

    # Method manage the autonomic drive
    def self_driving2(self, frame, mask_frame, process, system):

        # Drawing bounding box around the traffic sign
        AI.bounding_traffic_sign(self, frame, self.traffic_sign[1])

        # Get the traffic sign instruction
        temp_bool, max_speed = AI.traffic_sign_decoder(self, self.traffic_sign, 0)

        # Return threshold mask with 3 dim
        # mask = process.thresholding(frame)

        # Function return wrap image and points from bar
        warp_image, points = process.get_warp_image(mask_frame)

        # Function draw the points on the frame
        frame = process.draw_points(frame, np.array(points))

        # Draw color on the curve
        # inv_wrap, img_lane, frame = AI.draw_lane(frame, mask)

        # Calculate histogram of bottom curve
        mid_point, histogram_crop = process.get_histogram(frame, mask_frame, display=False, min_percent=0.5, region=4)

        # Calculate histogram of full curve
        average_point, histogram_curve = process.get_histogram(frame, mask_frame, display=False, min_percent=0.5, region=1)

        # Draw color on the curve
        inv_wrap, img_lane, frame = AI.draw_lane(frame, mask_frame)

        # Define the curve direction value
        curve_direction = mid_point - average_point

        # Find the right direction according to the lane
        speed, turn, time = AI.aim_car_direction(curve_direction, max_speed)

        # Define the frames in the main window
        # process.set_curve_frame(warp_image)
        # process.set_histogram_frame(frame)

        # speed, turn, time = 0, 0, 0

        # cv2.imshow("f", frame)
        # cv2.imshow("thr", mask_frame)
        # cv2.imshow("img_lane", img_lane)
        # cv2.imshow("inv_wrap", inv_wrap)
        # cv2.imshow("histogram_crop", histogram_crop)
        # cv2.imshow("histogram_curve", histogram_curve)
        # cv2.imshow("img_result", img_result)

        # frames = [frame, mask_frame, mask, warp_image, histogram_crop, histogram_curve, inv_wrap, img_lane]

        return frame, warp_image, speed, turn, time

    # Method manage the traffic sign command
    def traffic_sign_decoder(self, traffic_sign, area):

        if traffic_sign[0] in self.traffic_signs:
            # print("Area: ", area)
            # print("Traffic sign: ", traffic_sign)
            pass
        if traffic_sign[0] == "Speed limit (30km/h)":
            self.max_speed = 30
            # print("Area: ", area)
            # print("Speed: ", self.max_speed)
            # print("Traffic sign: ", traffic_sign)
        elif traffic_sign[0] == "Speed limit (50km/h)":
            self.max_speed = 50
            # print("Area: ", area)
            # print("Speed: ", self.max_speed)
            # print("Traffic sign: ", traffic_sign)
        elif traffic_sign[0] == "Stop":
            self.max_speed = 0
            # print("Area: ", area)
            # print("Speed: ", self.max_speed)
            # print("Traffic sign: ", traffic_sign)
        elif traffic_sign[0] == "No entry":
            # print("Area: ", area)
            # print("Traffic sign: ", traffic_sign)
            pass
        elif traffic_sign[0] == "Pedestrians":
            # print("Area: ", area)
            # print("Traffic sign: ", traffic_sign)
            pass

        return True, self.max_speed

    # Method draw bounding box around the traffic sign
    def bounding_traffic_sign(self, frame, coordinates):

        x, y, w, h = [int(coordinate) for coordinate in coordinates]

        if x != 0 and y != 0 and w != 0 and h != 0:

            self.traffic_sign[1] = [x, y, w, h]

            # cv2.drawContours(frame, contour, -1, (255, 0, 255), 7)
            cv2.rectangle(frame, (x-10, y-10), (x+w+10, y+h+10), (0, 255, 0), 5)

        return coordinates

    @staticmethod
    def draw_lane(frame, mask):

        # Create mask
        inv_wrap = mask.copy()

        # Remove some pixels
        inv_wrap[0:inv_wrap.shape[0]//2 + 25, 0:inv_wrap.shape[1]] = 0, 0, 0

        # Create green frame
        # img_lane = np.zeros_like(frame)
        img_lane = np.zeros(frame.shape, np.uint8)
        img_lane[:] = 0, 255, 0

        # Leave only the green pixels
        img_lane = cv2.bitwise_and(inv_wrap, img_lane)

        # Puts the two image one above the other
        img_result = cv2.addWeighted(frame, 1, img_lane, 1, 0)

        return inv_wrap, img_lane, img_result

    @staticmethod
    # Function aim the car speed
    def aim_car_direction(curve_row, max_speed):

        # sensitivity
        sen = 1.3

        # max speed
        max_speed /= 100
        # max_speed = 0.3

        # Average curve between [-1,1]
        average_curve = AI.get_average_curve(curve_row)

        if max_speed < average_curve:
            average_curve = max_speed
        if average_curve < -max_speed:
            average_curve = -max_speed

        if 0 < average_curve:
            sen = 1.7
            if average_curve < 0.05:
                average_curve = 0
        else:
            if -0.08 < average_curve:
                average_curve = 0

        time = 0.05
        speed = max_speed
        turn = round((-average_curve * sen), 3)

        # print("Speed: ", speed, " Turn: ", turn)
        return speed, turn, time

    @staticmethod
    # Method calculate the average
    def get_average_curve(curve_row):

        # Calculate the average curve
        if AI.average_values <= len(AI.curve_list):
            AI.curve_list.pop(0)

        AI.curve_list.append(curve_row)
        average_curve = int(sum(AI.curve_list) / len(AI.curve_list))

        # Normalize the value
        average_curve = average_curve / 100
        if 1 < average_curve:
            average_curve = 1
        if average_curve < -1:
            average_curve = -1

        return average_curve

    # Method collect data by saving frame with turn
    def collect_data(self, frame, turn, end_collect_data):

        if end_collect_data:
            collect_data = False
            AI.end_collect_data(self)
        else:
            collect_data = True
            self.model.collect_data(frame, turn)

        return collect_data

    # Method end collect data
    def end_collect_data(self):
        self.model.save_log()
