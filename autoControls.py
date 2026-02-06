# LEGO slot:0 autostart
from hub import port
import color, color_sensor, motor, runloop

# ---------------------------------------------------------------------------------------
# Global Variables
# ---------------------------------------------------------------------------------------
handMotor= port.E
colorSensor = port.A
neckMotor= port.F

hand_VELOCITY= 50

NECK_VELOCITY        = 30
DEFAULT_NECK_POSITION = 270

# --------------------------------------------------------------------------------------
# Colour Controls
# --------------------------------------------------------------------------------------
def is_blue():
    print ("Color Sensor Reading: Blue")
    return color_sensor.color(colorSensor) == color.BLUE

def is_red():
    print ("Color Sensor Reading: Red")
    return color_sensor.color(colorSensor) == color.RED

def is_black():
    print ("Color Sensor Reading: Black")
    return color_sensor.color(colorSensor) == color.BLACK

def is_no_color():
    print ("Color Sensor Reading: No Color")
    return color_sensor.color(colorSensor) == color.UNKNOWN
# --------------------------------------------------------------------------------------
# Neck Movement
#---------------------------------------------------------------------------------------
#async def nextBall():
    nextBallVelocity = 30
    print("Moving to next ball")
    motor.run_for_degrees(neckMotor, -30, nextBallVelocity)
    print ("At Next Position")
    await runloop.sleep_ms(500)

# --------------------------------------------------------------------------------------
# Hand Movement
#---------------------------------------------------------------------------------------
async def handDown(downPosition, downSpeed):
    downPosition = 0;
    print("\nMoving Hand Down")
    await motor.run_to_absolute_position(handMotor, downPosition, downSpeed)

async def handUp():
    upPosition = 260
    print("\nMoving Hand Up")
    await motor.run_to_absolute_position(handMotor, upPosition, hand_VELOCITY)

async def kick():
    print("\nKicking")
    await handUp();          await runloop.sleep_ms(100)
    await handDown(30, 200); await runloop.sleep_ms(100)
    await handUp();          await runloop.sleep_ms(100)
# ---------------------------------------------------------------------------------------
# Advanced Logic
#----------------------------------------------------------------------------------------
async def startUp():
    print("Starting Up...")
    await handUp(); await runloop.sleep_ms(500)
    await motor.run_to_absolute_position(neckMotor, DEFAULT_NECK_POSITION, NECK_VELOCITY, direction=motor.SHORTEST_PATH)
    print("At Home\n")
    await runloop.sleep_ms(500)


async def scoreGoal():
    scoringPosition = 320
    currentPosition = motor.absolute_position(neckMotor)

    await handDown(0, hand_VELOCITY)
    await motor.run_to_absolute_position(neckMotor, scoringPosition, 300, direction=motor.CLOCKWISE)
    await handUp()
    await motor.run_to_absolute_position(neckMotor, currentPosition, NECK_VELOCITY, direction=motor.COUNTERCLOCKWISE)
# ----------------------------------------------------------------------------------------
# Main Control Loop
# ---------------------------------------------------------------------------------------
async def main():

    # Startup Sequence
    await startUp()
    print("System Ready\n")

    while motor.absolute_position(neckMotor) < 70:
        await runloop.sleep_ms(100)
        if is_black() or is_no_color():
            print("\nBlack/No Color detected")
            motor.run_for_degrees(neckMotor, -30, NECK_VELOCITY)
        if is_blue():
            await scoreGoal()
            await runloop.sleep_ms(100)
        print(motor.absolute_position(neckMotor))
runloop.run(main())