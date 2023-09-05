
import cv2
import numpy as np

"Class manage the image display on the screen"


class Screen:

    if True:
        WIDTH, HEIGHT = 500, 350

    def __init__(self):

        # Define the background
        self.frame = Screen.initialize_frame(1)

    # Return black screen
    @staticmethod
    def initialize_frame(scale):
        return np.zeros((int(Screen.HEIGHT / scale), int(Screen.WIDTH / scale), 3), np.uint8)

    @staticmethod
    # Method display frames on the screen
    def display_window(frames, frame_size, window_shape):

        # Reshape all the frames to the same shape
        frames = Screen.reshape_frames(frames, frame_size, window_shape)

        # Collect all the frames to oen window
        main_window = Screen.collect_frames(frames, window_shape)

        # Plotting all the frames in one window
        cv2.imshow("Main_Window", main_window)

    @staticmethod
    # Method reshape all the frames to same shape
    def reshape_frames(frames, frame_size, window_shape):

        # Change all frames to 3 channels
        for i, frame in enumerate(frames):

            # Check if frame[3] is existed
            if len(frame.shape) < 3:
                # Adding 3-Dimension to the image
                frames[i] = frame[:, :, np.newaxis]

            # Function expand mask's dimension from 1 to 3 dimensions
            if frames[i].shape[2] < 3:
                frames[i] = np.repeat(frames[i], 3, axis=2)

            if frame.shape[0] != frame_size[0] or frame.shape[1] != frame_size[1]:
                frames[i] = cv2.resize(frames[i], (frame_size[1], frame_size[0]), interpolation=cv2.INTER_CUBIC)

        return frames

    @staticmethod
    # Method collect frames to one window
    def collect_frames(frames, window_shape):

        """window_shape = [height, width]"""

        main_window = Screen.initialize_frame(1)

        if window_shape == [1, 1]:
            main_window = frames[0]

        elif window_shape == [1, 2]:
            main_window = np.hstack((frames[0], frames[1]))

        elif window_shape == [1, 3]:
            # Create one window that contain: frame, tracking, mask
            main_window = np.hstack((frames[0], frames[1], frames[2]))

        if window_shape == [2, 3]:
            # Create one window that contain: frame, tracking, mask
            upper_window = np.hstack((frames[0], frames[1], frames[2]))

            # Create one window that contain: frame, tracking, mask
            lower_window = np.hstack((frames[3], frames[4], frames[5]))

            main_window = np.vstack((upper_window, lower_window))

        return main_window

