
"""Class object represent one path in the motor track"""


class Movement:

    # Drone speed must be between -100 ~ 100
    min_speed, max_speed = -100, 100

    def __init__(self, direction, sdk_speed, distance):

        # Distance - movement in cm
        # SDK Speed - the SDK value in the Tello.rc command
        # Direction - direction movement
        self.direction = direction
        self.sdk_speed = sdk_speed
        self.distance = distance

    # Return "Path(direction, speed, distance)"
    def __repr__(self):
        return f"Movement({self.__direction},{self.__sdk_speed},{self.__distance})"

    # Return "Movement(direction: direction, speed: speed, distance: distance)"
    def __str__(self):
        return f"Direction: {self.__direction}, Speed: {self.__sdk_speed}, Distance: {self.__distance}"

    @property
    def sdk_speed(self):
        return self.__sdk_speed

    @sdk_speed.setter
    def sdk_speed(self, speed):
        if (Movement.max_speed < speed) or (speed < Movement.min_speed):
            print("Speed must be between -100~100")
            self.__sdk_speed = 0
        else:
            self.__sdk_speed = speed

    # Return movement distance in cm
    @property
    def distance(self):
        return self.__distance

    # Set the movement distance in cm
    @distance.setter
    def distance(self, path_distance):
        self.__distance = path_distance

    # Return direction movement
    @property
    def direction(self):
        return self.__direction

    # Set direction movement
    @direction.setter
    def direction(self, path_direction):

        directions = ["Forward", "Backward", "Right", "Left", "Up", "Down", "Stand", "Rotate right", "Rotate left",
                      "Angular right forward", "Angular left forward", "Angular right backward", "Angular left backward"]

        if path_direction in directions:
            self.__direction = path_direction
        else:
            self.__direction = "Stand"
            print("CLASS: Movement - Invalid direction value")
