
import cv2
import numpy as np

from time import sleep


"Board Class represent the movement in the environment"


class Board:

    if True:
        # Define the font size as percent from the screen size
        FONT_SIZE = 0.50

        # Define frame size
        WIDTH, HEIGHT = 500, 350

        # Variables for start rows and cols to put text
        FIRST_COL = 5
        FIRST_ROW = 30
        LAST_ROW = int(HEIGHT - 10)
        LAST_COL = int(WIDTH - (WIDTH / 5))

    def __init__(self, board_frame):

        # Define the board size by extracting the frame shape
        self.height, self.width, _ = board_frame.shape

        self.board = np.zeros((self.height, self.width, 3), np.uint8)

        # Define the start location
        self.start_x = self.width // 2
        self.start_y = self.height // 2

        self.start_coordinate = [self.start_x, self.start_y]

        self.x_roi = self.start_x
        self.y_roi = self.start_y

    # Method initialize board frame
    def initialize_board_frame(self):

        # Clean pixels from last time we called the method
        self.board = np.zeros((self.height, self.width, 3), np.uint8)

    # Method put title on the frame
    def draw_title(self):

        # Plotting the frame title on the screen
        cv2.putText(self.board, "GPS", (Board.FIRST_COL, Board.FIRST_ROW), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)

    # Method check if point in the frame boundaries
    def in_boundaries(self, point):

        if 0 <= point[0] <= self.width and 0 <= point[1] <= self.height:
            return True
        else:
            return False

    # Method put text on the frame
    def draw_distance(self, point, coordinates):

        text_width, text_height = point[0] + 10, point[1] + 30

        # text_point = [text_width, text_height]
        clean_point = [text_width, text_height]

        # Check left and up boundaries
        if point[0] < self.width or self.height < point[0]:

            if point[0] < 0:
                text_width = 5
                clean_point[0] = 5
                clean_point[1] = text_height - 20
            if point[1] < 0:
                text_height = 25
                clean_point[0] -= 5
                clean_point[1] = 0

        # Check right and down boundaries
        if self.width < point[0] + 180 or self.height < point[1] + 50:

            if self.width < point[0] + 180:
                text_width = self.width - 170
                clean_point[0] = self.width - 180
                clean_point[1] = text_height - 20
            if self.height < point[1] + 50:
                text_height = self.height - 15
                # clean_point[0] = self.width - 15
                clean_point[1] = text_height - 20

        if 0 <= point[0] <= self.width and 0 <= point[1] <= self.height:

            # Drawing the location coordinates on the frame
            # cv2.putText(self.board,
            #             f'({(coordinates[-1][0] - self.start_x) / 25}, {-(coordinates[-1][1] - self.start_y) / 25})m',
            #             text_point, cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 255), 1)

            pass

        text_point = tuple([text_width, text_height])

        self.board[clean_point[1]:clean_point[1] + 30, clean_point[0]:clean_point[0] + 250] = 0

        # Drawing the location coordinates on the frame
        cv2.putText(self.board,
                    f'({(coordinates[-1][0] - self.start_x) / 25}, {-(coordinates[-1][1] - self.start_y) / 25})m',
                    text_point, cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 255), 1)

    # Method draw the user movements
    def draw_points(self, coordinates, motor_angle):

        end_drawing = False

        # Board.initialize_board_frame(self)

        Board.draw_title(self)

        # Draw lines between all the coordinates except the last two and return it
        new_point, last_point, point = Board.draw_tracks_lines(self, coordinates)

        while not end_drawing:

            # Clean the text for next iteration
            self.board[point[1]+10:point[1] + 40, point[0]+10:point[0] + 200] = 0

            # Return next point to draw
            end_drawing, point = Board.next_track_point(last_point, new_point)

            # Draw line between two points
            cv2.line(self.board, last_point, point, (0, 255, 0), 5)

            # Drawing the location coordinates on the frame
            Board.draw_distance(self, last_point, coordinates)

            self.x_roi, self.y_roi = last_point[0], last_point[1]

            # Update last point
            last_point = point

            # print("Class Board: draw_points: sleep may cause delay")
            sleep(0.01)

            # In case of draw angle needed
            if motor_angle < 0:
                pass
        # print(coordinates)
        return True, last_point

    # Method draw lines between previous points
    def draw_tracks_lines(self, coordinates):

        # Check coordinates array length
        last_point = tuple(coordinates[0])

        # Scan all the coordinates and draw it on the board
        for coordinate in coordinates[:-2]:

            # Every 25 cells is 1 meter. add 0.5 to round up / down
            x_coordinate = round((coordinate[0] - self.start_x))
            y_coordinate = round((coordinate[1] - self.start_y))

            # Define the coordinates as a point
            point = ((self.start_x + x_coordinate), (self.start_y + y_coordinate))

            # Check if the point coordinates is in the board boundaries
            if (0 < point[0] < self.width) or (0 < point[1] < self.height):
                cv2.line(self.board, last_point, point, (0, 255, 0), 5)

            # Update last point
            last_point = point

        return tuple(coordinates[-1]), tuple(coordinates[-2]), tuple(coordinates[-2])

    # Method return point to draw
    @staticmethod
    def next_track_point(last_point, new_point):

        point = last_point

        if last_point[0] < new_point[0]:
            point = (point[0] + 1, point[1])

        # Left movement
        if new_point[0] < last_point[0]:
            point = (point[0] - 1, point[1])

        # Down/Backward Movements
        if last_point[1] < new_point[1]:
            point = (point[0], point[1] + 1)

        # Up/Forward Movements
        if new_point[1] < last_point[1]:
            point = (point[0], point[1] - 1)

        if last_point[0] == new_point[0] and last_point[1] == new_point[1]:
            return True, point

        return False, point

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, board_width):
        self.__width = board_width

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, board_height):
        self.__height = board_height

    # Return np.zero()
    @property
    def board(self):
        return self.__board

    # Define board
    @board.setter
    def board(self, drone_board):
        self.__board = drone_board

    @property
    def start_x(self):
        return self.__start_x

    @start_x.setter
    def start_x(self, x):
        self.__start_x = x

    @property
    def start_y(self):
        return self.__start_y

    @start_y.setter
    def start_y(self, y):
        self.__start_y = y

    @property
    def start_coordinate(self):
        return self.start_coordinate

    @start_coordinate.setter
    def start_coordinate(self, point):
        self.__start_coordinate = point
        self.__start_x, self.__start_y = point[0], point[1]
