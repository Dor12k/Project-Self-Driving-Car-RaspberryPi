
from Movement import Movement


"Class represent a track"


class Track:

    meter = 25

    "Need to fix"
    start_x, start_y = 250, 175
    HOME = [start_x, start_y]

    # Collapse build-in tracks
    if True:

        # Patrol for 1,2,3 and 4 meters
        patrol_1m = [(start_x + meter, start_y), (start_x + meter, start_y - meter),
                     (start_x - meter, start_y - meter), (start_x - meter, start_y + meter),
                     (start_x + meter, start_y + meter), (start_x + meter, start_y), (start_x, start_y)]

        patrol_2m = [(start_x + 2 * meter, start_y), (start_x + 2 * meter, start_y - 2 * meter),
                     (start_x - 2 * meter, start_y - 2 * meter), (start_x - 2 * meter, start_y + 2 * meter),
                     (start_x + 2 * meter, start_y + 2 * meter), (start_x + 2 * meter, start_y), (start_x, start_y)]

        patrol_3m = [(start_x + 3 * meter, start_y), (start_x + 3 * meter, start_y - 3 * meter),
                     (start_x - 3 * meter, start_y - 3 * meter), (start_x - 3 * meter, start_y + 3 * meter),
                     (start_x + 3 * meter, start_y + 3 * meter), (start_x + 3 * meter, start_y), (start_x, start_y)]

        patrol_4m = [(start_x + 4 * meter, start_y), (start_x + 4 * meter, start_y - 4 * meter),
                     (start_x - 4 * meter, start_y - 4 * meter), (start_x - 4 * meter, start_y + 3 * meter),
                     (start_x + 4 * meter, start_y + 4 * meter), (start_x + 4 * meter, start_y), (start_x, start_y)]

        # Patrol for 1 meters
        patrol_clockwise_1m = [Movement("Right", 25, 50), Movement("Backward", 25, 50), Movement("Left", 25, 100),
                               Movement("Forward", 25, 100), Movement("Right", 25, 100),
                               Movement("Backward", 25, 50), Movement("Left", 25, 50)]

        # Patrol for 2 meters
        patrol_clockwise_2m = [Movement("Right", 25, 100), Movement("Backward", 25, 100), Movement("Left", 25, 200),
                               Movement("Forward", 25, 200), Movement("Right", 25, 200),
                               Movement("Backward", 25, 100), Movement("Left", 25, 100)]

        # Patrol for 6 meters
        patrol_clockwise_6m = [Movement("Right", 25, 300), Movement("Backward", 25, 300), Movement("Left", 25, 600),
                               Movement("Forward", 25, 600), Movement("Right", 25, 600),
                               Movement("Backward", 25, 300), Movement("Left", 25, 300)]

        # # Patrol 2 meters forward and backward
        patrol_fb_2m = [Movement("Forward", 50, 200), Movement("Stand", 50, 0), Movement("Backward", 25, 200)]

        # Patrol 4 meters forward and backward
        patrol_fb_4m = [Movement("Forward", 50, 400), Movement("Stand", 50, 0), Movement("Backward", 50, 400)]

        # Patrol 2 meters up and down
        patrol_ud_4m = [Movement("Up", 50, 400), Movement("Stand", 50, 0), Movement("Down", 50, 400)]

        patrol_angular = [Movement("Forward", 50, 800)]

    def __init__(self, motor_start_x, motor_start_y):

        # Variable store drone track movements
        self.motor_track = []

        # Define drone start location
        Track.start_x = motor_start_x
        Track.start_y = motor_start_y

        # Define drone home coordinates
        Track.HOME = [Track.start_x, Track.start_y]

    # Return track objects
    def __repr__(self):
        return f"Track: {self.motor_track}"

    # Return string from str method in Path class
    def __str__(self):

        track = "Track length: " + str(Track.get_length(self))

        for i, movement in enumerate(self.motor_track):
            track = track + "\n" + str(i) + ":   " + str(movement)

        return track

    # Return motor track
    @property
    def motor_track(self):
        return self.__motor_track

    # Set motor track
    @motor_track.setter
    def motor_track(self, track):
        self.__motor_track = track

    # Add Movement object
    def add_movement(self, movement):
        self.motor_track.append(movement)

    # Return track length
    def get_length(self):
        return len(self.motor_track)

    # Delete last path object from the track
    def delete_movement(self):
        self.motor_track.pop(-1)

    # Print the track
    def print_track(self):

        for path in self.motor_track:
            if path.get_direction() == -1:
                print("Stand")
            elif path.get_direction() == 0:
                if 0 < path.get_speed():
                    print("Right: ", path.get_distance(), "cm")
                else:
                    print("Left: ", path.get_distance(), "cm")
            elif path.get_direction() == 1:
                if 0 < path.get_speed():
                    print("Forward: ", path.get_distance(), "cm")
                else:
                    print("Backward: ", path.get_distance(), "cm")
            elif path.get_direction() == 2:
                if 0 < path.get_speed():
                    print("Up: ", path.get_distance(), "cm")
                else:
                    print("Down: ", path.get_distance(), "cm")
            elif path.get_direction() == 3:
                if 0 < path.get_speed():
                    print("Rotate Right: ", path.get_distance(), "degree")
                else:
                    print("Rotate Left: ", path.get_distance(), "degree")
