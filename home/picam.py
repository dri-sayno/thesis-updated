import time
import os
import glob
import RPi.GPIO as GPIO
from picamera import PiCamera


# FEEDER = 18
# CAMERA_BOTTOM = 25
# CAMERA_TOP = 23
# GLASS_UP = 21
# GLASS_DOWN = 12
# LEFT_FLASH = 5
# RIGHT_FLASH = 16

FEEDER = 18
CAMERA_BOTTOM = 23
CAMERA_TOP = 25
GLASS_UP = 12
GLASS_DOWN = 21
LEFT_FLASH = 5
RIGHT_FLASH = 16


def run(name, mode):
    if mode == 'ON':
        GPIO.output(name, GPIO.HIGH)
    else:
        GPIO.output(name, GPIO.LOW)


def sleep(seconds):
    time.sleep(seconds)


def capture_images(path, page_no, process):

    camera = PiCamera()
    number = int(page_no)
    ctr = 1
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)  # FEEDER
    GPIO.setup(23, GPIO.OUT)  # GLASS
    GPIO.setup(25, GPIO.OUT)  # GLASS REVERSE
    GPIO.setup(12, GPIO.OUT)  # CAMERA
    GPIO.setup(21, GPIO.OUT)  # CAMERA REVERSE
    GPIO.setup(5, GPIO.OUT)   # LEFT_FLASH
    GPIO.setup(16, GPIO.OUT)  # RIGHT_FLASH


    if process == 'feeder':
        for i in range(1, number * 2 + 1):
            image_name = 'image{0:02d}.jpg'.format(i)
            os.chdir(path)
            
            if (i % 2 == 0):
                print 'Capturing bottom image for page' + str(i)
                # Capture image with flash
                run(RIGHT_FLASH, 'ON')
                sleep(1)
                camera.start_preview()
                camera.capture(image_name)
                sleep(1)
                run(RIGHT_FLASH, 'OFF')

                print 'Dispensing paper ' + str(i)
                # Dispense paper and move cam to orig position
                run(GLASS_DOWN, 'ON')
                sleep(2)
                run(GLASS_DOWN, 'OFF')
                sleep(2)
                
                run(CAMERA_TOP, 'ON')
                sleep(2)
                run(CAMERA_TOP, 'OFF')
                sleep(2)
                
                print 'Reverting back to original position'
                # Move glass to orig position
                run(GLASS_UP, 'ON')
                sleep(2)
                run(GLASS_UP, 'OFF')

                sleep(2)
                #GPIO.cleanup()

            else:
                print 'Roller turned on ...'
                # Run roller to feed paper
                run(FEEDER, 'ON')
                sleep(6)
                run(FEEDER, 'OFF')
                print 'Roller turned off'

                print 'Capturing top image for page' + str(i)
                # Capture image with flash
                run(LEFT_FLASH, 'ON')
                sleep(1)
                camera.start_preview()
                camera.capture(image_name)
                sleep(1)
                run(LEFT_FLASH, 'OFF')

                print 'Moving camera to bottom position'
                # Move camera to bottom
                run(CAMERA_BOTTOM, 'ON')
                sleep(2)
                run(CAMERA_BOTTOM, 'OFF')
                sleep(2)

        camera.close()

    elif process == 'flatbed':
        # Count no of file on current dir
        fileCount = len(glob.glob1(path, "*.jpg"))

        os.chdir(path)
        sleep(1)

        # Run roller to feed paper
        run(FEEDER, 'ON')
        sleep(6)
        run(FEEDER, 'OFF')
        print 'Roller turned off'

        print 'Capturing top image for flatbed'
        # Capture top image of the page with flash
        run(LEFT_FLASH, 'ON')
        sleep(1)
        camera.start_preview()
        camera.capture('image{0:02d}.jpg'.format(fileCount + 1))
        sleep(1)
        run(LEFT_FLASH, 'OFF')
        
        print 'Moving camera to bottom position'
        # Move camera to bottom
        run(CAMERA_BOTTOM, 'ON')
        sleep(2)
        run(CAMERA_BOTTOM, 'OFF')
        
        print 'Capturing bottom image for flatbed'
        # Capture bottom image of the page with flash
        run(RIGHT_FLASH, 'ON')
        sleep(1)
        camera.start_preview()
        camera.capture('image{0:02d}.jpg'.format(fileCount + 2))
        sleep(1)
        run(RIGHT_FLASH, 'OFF')

        print 'Dispensing paper'
        # Dispense paper and move cam to orig position
        run(GLASS_DOWN, 'ON')
        sleep(2)
        run(GLASS_DOWN, 'OFF')
        sleep(2)

        run(GLASS_UP, 'ON')
        sleep(2)
        run(GLASS_UP, 'OFF')
        sleep(2)

        print 'Reverting camera to original position'
        run(CAMERA_TOP, 'ON')
        sleep(2)
        run(CAMERA_TOP, 'OFF')

        camera.close()
        GPIO.cleanup()
