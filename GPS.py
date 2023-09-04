
import math
import numpy as np

from Board import Board
from Tracks import Tracks
from Movement import Movement

"Class object represent a GPS and contain Tracks and Board object"


class GPS:

    if True:

        i = 0

        WIDTH, HEIGHT = 500, 350

    def __init__(self, sdk_movement_speed, sdk_angular_speed, sdk):

        self.driving = False

        # Store build-in tracks
        self.tracks = Tracks()

        self.last_cmd = "Stand"

        # Define the car start angle and coordinate
        self.gps_angle = 90

        # Counting the distance the motor did
        self.distance_path = 0

        # Counting the distance from the start point (0,0)
        self.distance_from_start = [0, 0]

        self.gps_track = self.tracks.GPS_track

        # Define angular sdk speed
        self.sdk_angular_speed = sdk_angular_speed

        # Define movement sdk speed
        self.sdk_movement_speed = sdk_movement_speed

        # Translate the sdk seed to real motion motor angular speed
        self.angular_speed = sdk_angular_speed * (self.sdk_angular_speed/sdk)

        # Translate the sdk seed to real motion motor speed
        self.movement_speed = sdk_movement_speed * (self.sdk_movement_speed/sdk)

        # Define board track
        self.board = Board(np.zeros((GPS.HEIGHT, GPS.WIDTH, 3), np.uint8))

        # Define the coordinates of car home
        self.home = [(self.board.start_x, self.board.start_y)]

        # Board_track is array of track coordinates
        self.board_track = [[self.board.start_x, self.board.start_y]]

        # Define right location of the car
        self.location = [self.board.start_x, self.board.start_y]

        self.x_coordinate, self.y_coordinate = self.board.start_x, self.board.start_y

    def update_gps(self, direction, distance, type_command, fix, fixed_distance, remote_control_event):

        # Update the movement data
        GPS.update_movement_data(self, direction, distance, type_command, fix, fixed_distance)

        # Draw the track in the GPS board
        complete, last_point = GPS.draw_track(self, type_command, remote_control_event)

        # If motor didn't finish the track (user interrupt) then update the data
        if not complete:
            self.board_track = self.board_track[:-1]
            fixed_distance = self.x_coordinate - last_point[0]
            GPS.update_movement_data(self, direction, distance, type_command, True, fixed_distance)

        return complete

    # Update data according to the drone movement
    def update_movement_data(self, direction, distance, type_command, fix, fixed_distance):

        # Initialize variables
        direction_factor = 0
        direction_constant = 1
        direction_multiplier = 1

        # Update direction variables
        if direction == "Forward":
            direction_factor = 1
            direction_constant = 0
            direction_multiplier = 1

        elif direction == "Backward":
            direction_factor = -1
            direction_constant = 0
            direction_multiplier = -1

        elif direction == "Right":
            direction_factor = 1
            direction_constant = -90
            direction_multiplier = 1

        elif direction == "Left":
            direction_factor = -1
            direction_constant = 90
            direction_multiplier = 1

        # In case user interrupt the track we fix the recent data
        if fix:
            self.distance_from_start[0] -= direction_factor * distance
            self.distance_path -= distance
            self.gps_track.delete_movement()
            distance = fixed_distance

        # Update drone flight distance
        self.distance_path += distance

        # Create movement object from Path class (direction, speed, distance)
        movement = Movement(direction, self.sdk_movement_speed, distance)

        # Add movement to the drone track
        self.gps_track.add_movement(movement)

        # Update the distance from the start point
        self.distance_from_start[0] += direction_factor * distance

        d_x = round(distance * math.cos(math.radians(self.gps_angle + direction_constant)))
        d_y = round(distance * math.sin(math.radians(self.gps_angle + direction_constant)))

        # Type command 1 mean command came from keyboard and 2 from build-in track
        if type_command == 1 or type_command == 2:
            d_x = round(d_x / 4)
            d_y = round(d_y / 4)

        # Update drone location
        self.location = [self.x_coordinate + direction_multiplier * d_x, self.y_coordinate - direction_multiplier * d_y]

    # Draw motor board track on the board
    def draw_track(self, type_command, remote_control_event):

        # Draw the track in the drone board
        # if type_command = 0 is mean the command came from board track
        # if type_command = 1 is mean the command came from user keyboard
        # if type_command = 2 is mean the command came from motor track
        # Function return flag if motor finish the track or get interrupt by the user
        if type_command == 0:
            complete, point = self.board.draw_tracks(self.board_track, self.gps_angle, remote_control_event)
        elif type_command == 1:
            complete, point = self.board.draw_points(self.board_track, self.gps_angle)
        elif type_command == 2:
            complete, point = self.board.draw_tracks(self.board_track, self.gps_angle, remote_control_event)
        else:
            complete, point = True, self.location

        return complete, point

    "GPS Function"

    @property
    def movement_speed(self):
        return self.__movement_speed

    @movement_speed.setter
    def movement_speed(self, drone_movement_speed):
        self.__movement_speed = drone_movement_speed

    @property
    def angular_speed(self):
        return self.__angular_speed

    @angular_speed.setter
    def angular_speed(self, drone_angular_speed):
        self.__angular_speed = drone_angular_speed

    @property
    def sdk_angular_speed(self):
        return self.__sdk_angular_speed

    @sdk_angular_speed.setter
    def sdk_angular_speed(self, drone_sdk_angular_speed):
        if 100 < drone_sdk_angular_speed or drone_sdk_angular_speed < -100:
            print("Class Drone: sdk speed must be between -100~100")
            self.__sdk_angular_speed = 0
        else:
            self.__sdk_angular_speed = drone_sdk_angular_speed

    @property
    def sdk_movement_speed(self):
        return self.__sdk_movement_speed

    @sdk_movement_speed.setter
    def sdk_movement_speed(self, drone_sdk_movement_speed):
        if 100 < drone_sdk_movement_speed or drone_sdk_movement_speed < -100:
            print("Class Drone: sdk speed must be between -100~100. value: ", drone_sdk_movement_speed)
            self.__sdk_movement_speed = 0
        else:
            self.__sdk_movement_speed = drone_sdk_movement_speed

    # Return drone angle
    @property
    def gps_angle(self):
        return self.__gps_angle

    # Set drone angle
    @gps_angle.setter
    def gps_angle(self, angle):

        self.__gps_angle = angle

        if 360 < self.__gps_angle:
            self.__gps_angle = float(self.__gps_angle - 360)
        if self.__gps_angle < -360:
            self.__gps_angle = float(self.__gps_angle + 360)

    # Get the track the drone did as array of Path objects
    @property
    def gps_track(self):
        # Drone track is a Track object
        return self.__gps_track

    # Set the track the drone did
    @gps_track.setter
    def gps_track(self, track):
        # track should be Track object
        self.__gps_track = track

    # Return the track the drone did as array of coordinates
    @property
    def board_track(self):
        return self.__board_track

    # Set the track drone did as array od coordinates
    @board_track.setter
    def board_track(self, track):
        self.__board_track = track

    # Return drone board which is numpy array
    @property
    def board(self):
        return self.__board

    @board.setter
    def board(self, drone_board):
        self.__board = drone_board

    # Return the path distance
    @property
    def distance_path(self):
        return self.__distance_path

    # Update the path distance
    @distance_path.setter
    def distance_path(self, distance):
        if distance == 0:
            self.__distance_path = distance
        else:
            self.__distance_path = self.distance_path + distance

    # Get distance from start point
    @property
    def distance_from_start(self):
        return self.__distance_from_start

    # Update the distance from start point
    @distance_from_start.setter
    def distance_from_start(self, distance):
        self.__distance_from_start = distance

    # Get drone coordinate location as point (x, y)
    @property
    def location(self):
        return self.__location

    # Set drone coordinate location
    @location.setter
    def location(self, coordinate):

        self.__location = [coordinate[0], coordinate[1]]

        self.x_coordinate, self.y_coordinate = self.location[0], self.location[1]

        # Add current coordinate to the board track array
        self.board_track.append(self.location)

    # Get x coordinate
    @property
    def x_coordinate(self):
        return self.__x_coordinate

    # Set x coordinate
    @x_coordinate.setter
    def x_coordinate(self, x):
        self.__x_coordinate = x
        self.location[0] = self.__x_coordinate

    # Get y coordinate
    @property
    def y_coordinate(self):
        return self.__y_coordinate

    # Set y coordinate
    @y_coordinate.setter
    def y_coordinate(self, y):
        self.__y_coordinate = y
        self.location[1] = self.__y_coordinate
