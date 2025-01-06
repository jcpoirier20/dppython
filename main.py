from machine import Pin, PWM
import time

# HOME: hands open, wrists go to zero; Home is to load a sandwich
# GRASP: Closes both hands to a closed position to hold the sandwich
# FORWARD: The system executes a series of moves to move the sandwich forward
# First: LeftHand opens, leftWrist rotates away from user, then closes
# Second: RightHand opens, LeftWrist rotate forward into home position, then right hand closes
# FORWARD: Same as before, but leads with the right hand

# wrist movement and hand movment in degrees is already defined in CPP code. Go find it.
# Check with Robotis about the dynamixel servos and their movement in degrees

# Constants
ENABLE2PASSFEEDFORWARD = None # potentially a boolean that would become true if the feedforward button was allowed to be pressed/executed
OFFSET = 180 # servo rotation in degrees before product assembly TODO: What is "before product assembly?" No idea. Seems unnecessary until we know how the servos are oriented
HAND_HOME = OFFSET
HAND_OPEN = HAND_HOME
HAND_HALF_OPEN = HAND_HOME + 45
HAND_CLOSED = HAND_HOME + 90
WRIST_RANGE = 12 if ENABLE2PASSFEEDFORWARD else 25 # total wrist movement in degrees
WRIST_HOME = OFFSET
WRIST_TURNED = WRIST_HOME + WRIST_RANGE
REVERSE_DIRECTION = True

# Define the states
BEGIN = 0
ROTATE_WRIST_BACK = 1
CLOSE_HAND = 2
OPEN_OTHER_HAND = 3
ROTATE_WRIST_FRONT = 4
CLOSE_OTHER_HAND = 5

# Initialize the state
state = BEGIN
busy = False

# Define stateful devices
led = Pin(13, Pin.OUT)

print("LED program starting...")

while True:
    print("LED ON")
    led.value(1)  # Explicitly turn ON
    time.sleep(1)
    
    print("LED OFF")
    led.value(0)  # Explicitly turn OFF
    time.sleep(1)

# Define the Hand and Wrist classes with necessary methods
class Hand:
    def __init__(self, pin):
        self.servo = PWM(Pin(pin), freq=50)
        self.position = 0

    def open_halfway(self):
        self.servo.duty(75)  # Example duty cycle for halfway open
        self.position = 75

    def close(self):
        self.servo.duty(0)  # Example duty cycle for closed
        self.position = 0

    def is_moving(self):
        # Placeholder for actual movement detection logic
        return False

class Wrist:
    def __init__(self, pin):
        self.servo = PWM(Pin(pin), freq=50)
        self.position = 0

    def goto_position1(self):
        self.servo.duty(150)  # Example duty cycle for position 1
        self.position = 150

    def go_home(self):
        self.servo.duty(0)  # Example duty cycle for home position
        self.position = 0

    def is_moving(self):
        # Placeholder for actual movement detection logic
        return False

# Initialize the hands and wrists
hand = [Hand(26), Hand(25)]
wrist = [Wrist(33), Wrist(32)]

# Main loop
while True:
    if state == BEGIN:
        busy = True
        print("\nFeedForward\tBegin")

        # Open the hand enough to clear the sandwich
        hand[0].open_halfway()
        print("Finished Begin, Start Hand[0].OpenHalfway()")
        state = ROTATE_WRIST_BACK

    elif state == ROTATE_WRIST_BACK:
        # Wait for the hand to clear before moving the wrist
        if hand[0].is_moving():
            continue

        # Rotate the wrist to the back
        wrist[0].goto_position1()
        print("Finished RotateWristBack, Start Wrist[0].GotoBack")
        state = CLOSE_HAND

    elif state == CLOSE_HAND:
        # Wait for the wrist to stop moving before closing the hand
        if wrist[0].is_moving():
            continue

        # Close the hand
        hand[0].close()
        print("Finished CloseHand, Start Hand[0].Close()")
        state = OPEN_OTHER_HAND

    elif state == OPEN_OTHER_HAND:
        # Wait for the hand to close before opening the other hand
        if hand[0].is_moving():
            continue

        # Open the other hand
        hand[1].open_halfway()
        print("Finished OpenOtherHand, Start Hand[1].OpenHalfway()")
        state = ROTATE_WRIST_FRONT

    elif state == ROTATE_WRIST_FRONT:
        # Wait for the other hand to open before rotating the wrist
        if hand[1].is_moving():
            continue

        # Rotate the wrist to the front position
        wrist[0].go_home()
        print("Finished RotateWristFront, Start Wrist[0].GotoFront")
        state = CLOSE_OTHER_HAND

    elif state == CLOSE_OTHER_HAND:
        # Wait for the wrist to stop moving before closing the other hand
        if wrist[0].is_moving():
            continue

        # Close the other hand
        hand[1].close()
        print("Finished CloseOtherHand, Start Hand[1].Close()")
        state = BEGIN

    time.sleep(0.1)  # Small delay to prevent busy-waiting