
from Track import Track
from Movement import Movement


class Tracks:

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
        patrol_clockwise_1m = Track(start_x, start_y)
        patrol_clockwise_1m.add_movement(Movement("Right", 25, 50))
        patrol_clockwise_1m.add_movement(Movement("Backward", 25, 50))
        patrol_clockwise_1m.add_movement(Movement("Left", 25, 100))
        patrol_clockwise_1m.add_movement(Movement("Forward", 25, 100))
        patrol_clockwise_1m.add_movement(Movement("Right", 25, 100))
        patrol_clockwise_1m.add_movement(Movement("Backward", 25, 50))
        patrol_clockwise_1m.add_movement(Movement("Left", 25, 50))

        # Patrol for 2 meters
        patrol_clockwise_2m = Track(start_x, start_y)
        patrol_clockwise_2m.add_movement(Movement("Right", 25, 100))
        patrol_clockwise_2m.add_movement(Movement("Backward", 25, 100))
        patrol_clockwise_2m.add_movement(Movement("Left", 25, 200))
        patrol_clockwise_2m.add_movement(Movement("Forward", 25, 200))
        patrol_clockwise_2m.add_movement(Movement("Right", 25, 200))
        patrol_clockwise_2m.add_movement(Movement("Backward", 25, 100))
        patrol_clockwise_2m.add_movement(Movement("Left", 25, 100))

        # Patrol for 6 meters
        patrol_clockwise_6m = Track(start_x, start_y)
        patrol_clockwise_6m.add_movement(Movement("Right", 25, 300))
        patrol_clockwise_6m.add_movement(Movement("Backward", 25, 300))
        patrol_clockwise_6m.add_movement(Movement("Left", 25, 600))
        patrol_clockwise_6m.add_movement(Movement("Forward", 25, 600))
        patrol_clockwise_6m.add_movement(Movement("Right", 25, 600))
        patrol_clockwise_6m.add_movement(Movement("Backward", 25, 300))
        patrol_clockwise_6m.add_movement(Movement("Left", 25, 300))

        # # Patrol 2 meters forward and backward
        patrol_fb_2m = Track(start_x, start_y)
        patrol_fb_2m.add_movement(Movement("Forward", 50, 200))
        patrol_fb_2m.add_movement(Movement("Stand", 50, 0))
        # patrol_fb_2m.add_path(Path("backward", 25, 200))

        # Patrol 4 meters forward and backward
        patrol_fb_4m = Track(start_x, start_y)
        patrol_fb_4m.add_movement(Movement("Forward", 50, 400))
        patrol_fb_4m.add_movement(Movement("Stand", 50, 0))
        patrol_fb_4m.add_movement(Movement("Backward", 50, 400))

        # Patrol 2 meters up and down
        patrol_ud = Track(start_x, start_y)
        patrol_ud.add_movement(Movement("Up", 50, 400))
        patrol_ud.add_movement(Movement("Stand", 50, 0))
        # patrol_ud.add_movement(Movement("Down", 50, 400))

        patrol_angular = Track(start_x, start_y)
        patrol_angular.add_movement(Movement("Forward", 50, 800))

    def __init__(self):
        self.GPS_track = Track(Tracks.start_x, Tracks.start_y)
