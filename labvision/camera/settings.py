import cv2

LOGITECH_HD_1080P = {
    'res': ((1920, 1080, 3), (640, 480, 3), (1280, 720, 3), (480, 360, 3)),
    'fps': ((30.0),)
}

PHILIPS3 = {
    'res': ((640, 480, 3), (1280, 1080, 3)),
    'fps': ((20.0),)
}

MIKELAPTOP = {
    'res': ((640, 480, 3)),
    'fps': ((20.0),)
}

'''
Settings for the Nikon camera are entered directly into the settings_script nikon.
You may need to change permissions to make this executable.
'''
NIKON_DSCOOLPIX_9600 = {
    'script':'nikon_config.sh'
}