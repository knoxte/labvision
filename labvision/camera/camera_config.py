

'''
Web camera settings
All settings are accessible via self.cam_type in CameraBase class
Only required settings are 1 resolution and 1 fps.
Can add any optional info you want.
'''

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
Digital Camera settings
Acquisition settings for digital cameras need their own script.
See nikon_config.sh for example in scripts folder.
You may need to change permissions to make this file executable.
'''
NIKON_DSCOOLPIX_9600 = {
    'script': 'scripts/nikon_config.sh',
    'min_delay': 1
}