
import math
import threading

from GPS import GPS
from time import sleep

"Class object represent a motor and contain GPS object"


class Motor:

    if True:

        i = 0

        # The movements speed test performed with SDK_SPEED = 50
        SDK_SPEED = 50

        # Motor do 0.78 cm/sec
        speed_unit = float(39/50)

        # Store the motor SDK speed
        motor_sdk_angular_speed = 20
        motor_sdk_movement_speed = 20

        # Represent speed
        motor_angular_speed = 360 / 10  # Angular speed degrees/s (50d/s)
        motor_movement_speed = 390 / 10  # Forward speed in cm/s (50cm/s)

    def __init__(self, enable_a, in1_a, in2_a, enable_b, in1_b, in2_b):

        # Define angular sdk speed
        self.sdk_angular_speed = Motor.motor_sdk_angular_speed

        # Define movement sdk speed
        self.sdk_movement_speed = Motor.motor_sdk_movement_speed

        # # Translate the sdk seed to real motion motor angular speed
        self.angular_speed = Motor.motor_angular_speed * (self.sdk_angular_speed/Motor.SDK_SPEED)

        # Translate the sdk seed to real motion motor speed
        self.movement_speed = Motor.motor_movement_speed * (self.sdk_movement_speed/Motor.SDK_SPEED)

        # GPS object drawing the track of the motor
        self.GPS = GPS(self.sdk_movement_speed, self.sdk_angular_speed, Motor.SDK_SPEED)

        # Hold motor status
        self.driving = False

        # Hold last motor command
        self.last_cmd = "Stand"

        # Motor setup
        if True:

            self.enable_a = enable_a
            self.in1_a = in1_a
            self.in2_a = in2_a

            self.enable_b = enable_b
            self.in1_b = in1_b
            self.in2_b = in2_b

            # GPIO.setup(self.enable_a, GPIO.OUT)
            # GPIO.setup(self.in1_a, GPIO.OUT)
            # GPIO.setup(self.in2_a, GPIO.OUT)

            # GPIO.setup(self.enable_b, GPIO.OUT)
            # GPIO.setup(self.in1_b, GPIO.OUT)
            # GPIO.setup(self.in2_b, GPIO.OUT)

            # self.pwmA = GPIO.PWM(self.enable_a, 100);
            # self.pwmA.start(0)

            # self.pwmB = GPIO.PWM(self.enable_b, 100);
            # self.pwmB.start(0)

    def driving_manager(self, system, thread_event):

        if system.self_driving:

            # Send command to flight right
            t = threading.Thread(target=Motor.self_driving, args=(self, system.speed, system.turn, system.time), daemon=True)
            t.name = "thread_name " + str(Motor.i)
            t.start()

            Motor.i += 1
        else:

            # Send command to flight right
            t = threading.Thread(target=Motor.user_driving, args=(self, system.speed, system.turn, system.time, 1, thread_event), daemon=True)
            t.name = "thread_name " + str(Motor.i)
            t.start()

            Motor.i += 1

        return Motor.get_gps(self)

    def self_driving(self, speed=0.5, turn=0, time=0):

        distance = 10
        command_type = 1
        remote_control_event = None
        speed, turn, right_speed, left_speed = Motor.aim_motion_values(speed, turn, time)
        # speed, turn, time, right_speed, left_speed = 0, 0, 0, 0, 0

        # print("Speed: ", speed, " Left Speed: ", left_speed, " Right Speed: ", right_speed, " Turn: ", turn)

        if speed == 0:
            return Motor.stand(self)
        elif turn == 0 < speed:
            return Motor.move_forward(self, distance, command_type, remote_control_event)
        elif speed < 0 == turn:
            return Motor.move_backward(self, distance, command_type, remote_control_event)

        elif left_speed < 0 < right_speed:
            return Motor.move_reverse_left(self, distance, command_type, remote_control_event)
        elif right_speed < 0 < left_speed:
            return Motor.move_reverse_right(self, distance, command_type, remote_control_event)

        elif 0 < left_speed and 0 < right_speed:
            if turn < 0 < speed:
                return Motor.move_left(self, distance, command_type, remote_control_event)
            if 0 < turn and 0 < speed:
                return Motor.move_right(self, distance, command_type, remote_control_event)

    def user_driving(self, speed, turn, time, command_type, remote_control_event):
        distance = 39

        if speed == 0:
            return Motor.stand(self)
        elif turn == 0 < speed:
            return Motor.move_forward(self, distance, command_type, remote_control_event)
        elif speed < 0 == turn:
            return Motor.move_backward(self, distance, command_type, remote_control_event)

        elif 0 < turn and 0 < speed:
            return Motor.move_right(self, distance, command_type, remote_control_event)
        elif turn < 0 < speed:
            return Motor.move_left(self, distance, command_type, remote_control_event)
        elif turn < 0 and speed < 0:
            return Motor.move_reverse_right(self, distance, command_type, remote_control_event)
        elif speed < 0 < turn:
            return Motor.move_reverse_left(self, distance, command_type, remote_control_event)

    def move_forward(self, distance, command_type, remote_control_event):
        if not self.last_cmd == "Forward":
            self.last_cmd = "Forward"

            # Make the movement from Motion class
            tf = threading.Thread(target=Motor.motor_forward, args=(self, distance))
            tf.name = "Motor: Forward"
            tf.start()

            # Update the movement data
            tfg = threading.Thread(target=self.GPS.update_gps, args=("Forward", distance, command_type, False, 0, remote_control_event,), daemon=True)
            tfg.name = "Motor: GPS Forward"
            tfg.start()
            complete = True

            tf.join()
            tfg.join()

            # Finish movement with stand in place
            Motor.stand(self)
        else:
            complete = False
        return complete

    def move_backward(self, distance, command_type, remote_control_event):
        if not self.last_cmd == "Backward":
            self.last_cmd = "Backward"

            # Make the movement from Motion class
            tb = threading.Thread(target=Motor.motor_backward, args=(self, distance))
            tb.name = "Motor: Backward"
            tb.start()

            # Update the movement data
            tbg = threading.Thread(target=self.GPS.update_gps, args=("Backward", distance, command_type, False, 0, remote_control_event,), daemon=True)
            tbg.name = "Motor: GPS Backward"
            tbg.start()
            complete = True

            tb.join()
            tbg.join()

            # Finish movement with stand in place
            Motor.stand(self)
        else:
            complete = False
        return complete

    def move_right(self, distance, command_type, remote_control_event):
        if not self.last_cmd == "Right":
            self.last_cmd = "Right"

            # Make the movement from Motion class
            tr = threading.Thread(target=Motor.motor_right, args=(self, distance))
            tr.name = "Motor: Right"
            tr.start()

            # Update the movement data
            trg = threading.Thread(target=self.GPS.update_gps, args=("Right", distance, command_type, False, 0, remote_control_event))
            trg.name = "Motor: GPS Right"
            trg.start()
            complete = True

            tr.join()
            trg.join()

            # Finish movement with stand in place
            Motor.stand(self)
        else:
            complete = False
        return complete

    def move_left(self, distance, command_type, remote_control_event):
        if not self.last_cmd == "Left":
            self.last_cmd = "Left"

            # Make the movement from Motion class
            tl = threading.Thread(target=Motor.motor_left, args=(self, distance))
            tl.name = "Motor: Left"
            tl.start()

            # Update the movement data
            tlg = threading.Thread(target=self.GPS.update_gps, args=("Left", distance, command_type, False, 0, remote_control_event))
            tlg.name = "Motor: GPS"
            tlg.start()

            tl.join()
            tlg.join()

            complete = True

            # Finish movement with stand in place
            Motor.stand(self)
        else:
            complete = False
        return complete

    def move_reverse_right(self, distance, command_type, remote_control_event):
        if not self.last_cmd == "Reverse Right":
            self.last_cmd = "Reverse Right"

            # Make the movement from Motion class
            trr = threading.Thread(target=Motor.motor_reverse_left, args=(self, distance))
            trr.name = "Motor: Reverse Right"
            trr.start()

            # Update the movement data
            rrg = threading.Thread(target=self.GPS.update_gps, args=("Reverse Right", distance, command_type, False, 0, remote_control_event))
            rrg.name = "Motor: GPS Reverse Right"
            rrg.start()

            trr.join()
            rrg.join()

            complete = True

            # Finish movement with stand in place
            Motor.stand(self)
        else:
            complete = False
        return complete

    def move_reverse_left(self, distance, command_type, remote_control_event):
        if not self.last_cmd == "Reverse Left":
            self.last_cmd = "Reverse Left"

            # Make the movement from Motion class
            trl = threading.Thread(target=Motor.motor_reverse_left, args=(self, distance))
            trl.name = "Motor: Reverse Left"
            trl.start()

            # Update the movement data
            rlg = threading.Thread(target=self.GPS.update_gps, args=("Reverse Left", distance, command_type, False, 0, remote_control_event))
            rlg.name = "Motor: GPS Reverse Right"
            rlg.start()

            complete = True

            trl.join()
            rlg.join()

            # Finish movement with stand in place
            Motor.stand(self)
        else:
            complete = False
        return complete

    def stand(self):

        # Update motor last command
        if not self.last_cmd == "Stand":
            self.last_cmd = "Stand"

            self.motor_stand()

    def stop(self, time):
        # self.pwmA.ChangeDutyCycle(0)
        # self.pwmB.ChangeDutyCycle(0)
        pass

    def motor_forward(self, distance):

        # If drone is already flying  do nothing
        if not self.last_cmd == "Forward":

            # Updating the last command
            self.last_cmd = "Forward"

            # Calculate time according to time = distance/speed
            timer = abs(float(distance / self.movement_speed))

            # Send forward command to the drone SDK
            # GPIO.output(self.in1_a, GPIO.HIGH)
            # GPIO.output(self.in2_a, GPIO.LOW)
            # GPIO.output(self.in1_b, GPIO.HIGH)
            # GPIO.output(self.in2_b, GPIO.LOW)

            # self.pwmA.ChangeDutyCycle(abs(left_speed))
            # self.pwmB.ChangeDutyCycle(abs(right_speed))

            # Sleep for the time that taking to flight
            # sleep(timer)
        return

    def motor_backward(self, distance):

        # If drone is already flying  do nothing
        if not self.last_cmd == "Backward":
            # Updating the last command
            self.last_cmd = "Backward"

            # Calculate time according to time = distance/speed
            timer = abs(float(distance / self.movement_speed))

            # Send backward command to the drone SDK
            # GPIO.output(self.in1_a, GPIO.LOW)
            # GPIO.output(self.in2_a, GPIO.HIGH)
            # GPIO.output(self.in1_b, GPIO.LOW)
            # GPIO.output(self.in2_b, GPIO.HIGH)

            # self.pwmA.ChangeDutyCycle(abs(left_speed))
            # self.pwmB.ChangeDutyCycle(abs(right_speed))

            # Sleep for the time that taking to flight
            # sleep(timer)
        return

    def motor_right(self, distance):

        # If drone is already flying  do nothing
        if not self.last_cmd == "Right":
            # Updating the last command
            self.last_cmd = "Right"

            # Calculate time according to time = distance/speed
            timer = abs(float(distance / self.movement_speed))

            # Send right command to the drone SDK
            # GPIO.output(self.in1_a, GPIO.HIGH)
            # GPIO.output(self.in2_a, GPIO.LOW)
            # GPIO.output(self.in1_b, GPIO.HIGH)
            # GPIO.output(self.in2_b, GPIO.LOW)

            # self.pwmA.ChangeDutyCycle(abs(left_speed))
            # self.pwmB.ChangeDutyCycle(abs(right_speed))

            # Sleep for the time that taking to flight
            # sleep(timer)
        return

    def motor_left(self, distance):

        # If drone is already flying  do nothing
        if not self.last_cmd == "Left":
            # Updating the last command
            self.last_cmd = "Left"

            # Calculate time according to time = distance/speed
            timer = abs(float(distance / self.movement_speed))

            # Send left command to the drone SDK
            # GPIO.output(self.in1_a, GPIO.HIGH)
            # GPIO.output(self.in2_a, GPIO.LOW)
            # GPIO.output(self.in1_b, GPIO.HIGH)
            # GPIO.output(self.in2_b, GPIO.LOW)

            # self.pwmA.ChangeDutyCycle(abs(left_speed))
            # self.pwmB.ChangeDutyCycle(abs(right_speed))

            # Sleep for the time that taking to flight
            # sleep(timer)
        return

    def motor_reverse_right(self, distance):

        # If drone is already flying  do nothing
        if not self.last_cmd == "Reverse Right":
            # Updating the last command
            self.last_cmd = "Reverse Right"

            # Calculate time according to time = distance/speed
            timer = abs(float(distance / self.movement_speed))

            # Send right command to the drone SDK
            # GPIO.output(self.in1_a, GPIO.HIGH)
            # GPIO.output(self.in2_a, GPIO.LOW)
            # GPIO.output(self.in1_b, GPIO.LOW)
            # GPIO.output(self.in2_b, GPIO.HIGH)

            # self.pwmA.ChangeDutyCycle(abs(left_speed))
            # self.pwmB.ChangeDutyCycle(abs(right_speed))

            # Sleep for the time that taking to flight
            sleep(timer)
        return

    def motor_reverse_left(self, distance):

        # If drone is already flying  do nothing
        if not self.last_cmd == "Reverse Left":
            # Updating the last command
            self.last_cmd = "Reverse Left"

            # Calculate time according to time = distance/speed
            timer = abs(float(distance / self.movement_speed))

            # Send left command to the drone SDK
            # GPIO.output(self.in1_a, GPIO.LOW)
            # GPIO.output(self.in2_a, GPIO.HIGH)
            # GPIO.output(self.in1_b, GPIO.HIGH)
            # GPIO.output(self.in2_b, GPIO.LOW)

            # self.pwmA.ChangeDutyCycle(abs(left_speed))
            # self.pwmB.ChangeDutyCycle(abs(right_speed))

            # Sleep for the time that taking to flight
            sleep(timer)
        return

    def motor_stand(self):

        # Update drone last command
        if not self.last_cmd == "Stand":
            self.last_cmd = "Stand"

            # Make the movement from Motion class
            # self.pwmA.ChangeDutyCycle(0)
            # self.pwmB.ChangeDutyCycle(0)

            sleep(0.1)

    @staticmethod
    def aim_motion_values(speed=0.5, turn=0, time=0):

        turn *= 100
        speed *= 100
        left_speed = speed - turn
        right_speed = speed + turn

        if 100 < left_speed:
            left_speed = 100
        elif left_speed < -100:
            left_speed = -100

        if 100 < right_speed:
            right_speed = 100
        elif right_speed < -100:
            right_speed = -100

        # Short the float number
        left_speed = abs(math.trunc(left_speed))
        right_speed = abs(math.trunc(right_speed))

        # sleep(time)
        # print("Speed: ", speed, " Left Speed: ", left_speed, " Right Speed: ", right_speed, " Turn: ", turn)
        return speed, turn, right_speed, left_speed

    # Method return GPS frame
    def get_gps(self):
        return self.GPS.board.board

    # Method send motor to patrol
    def patrol(self):
        pass
