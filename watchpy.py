import pygame, sys, time
import pygame.camera
from pygame.locals import *

# Include the Dropbox SDK libraries
from dropbox import client, rest, session

# Get your app key and secret from the Dropbox developer website
APP_KEY = 'YourKeyHere'
APP_SECRET = 'YourSecretHere'

# ACCESS_TYPE should be 'dropbox' or 'app_folder' as configured for your app
ACCESS_TYPE = 'app_folder'

sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)

request_token = sess.obtain_request_token()

# Make the user sign in and authorize this token
url = sess.build_authorize_url(request_token)
print url
print "Please authorize in the browser. After you're done, press enter."
raw_input()

# This will fail if the user didn't visit the above URL and hit 'Allow'
access_token = sess.obtain_access_token(request_token)

client = client.DropboxClient(sess)
print "linked account : \n", client.account_info(), "\n"

#capture

def capture():
    #init pygame
    pygame.init()
    
    #setup font
    WHITE = 255,255,255
    font_med = pygame.font.Font(None, 25)
    
    #init cam
    pygame.camera.init()
    camSize = (640, 480)
    cam = pygame.camera.Camera("/dev/video0", camSize, "RGB")
    cam.start()
    
    #capture image
    img = cam.get_image()
    now = time.localtime(time.time())
    timecode = time.strftime("%a %b %d %Y - %H:%M:%S", now)
    
    text_surface = font_med.render(timecode, True, WHITE)
    rect = text_surface.get_rect(center=(320,460))
    img.blit(text_surface, rect)
    
    #saving image
    filename = "%s.jpeg" % (timecode)
    pygame.image.save(img,filename)
    print "image saved at ", timecode
    
    #stopping camera & exiting pygame
    cam.stop()
    pygame.quit()

    return filename

    
def uploadDropbox(filename):
    #copy to dropbox
    try:
        f = open(filename)
        response = client.put_file(filename, f)
        print "uploaded to dropbox"#, response
        f.close()
    except:
        print "Error during the upload to dropbox"



#main loop
while True:
    name = capture()
    uploadDropbox(name)
    time.sleep(60)


