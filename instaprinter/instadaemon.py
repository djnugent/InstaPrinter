import threading
import time
import subprocess
import os
from queue import Queue
from instauser import User
from instarender import InstagramTheme
from instaparser import InstagramPost

POLL_RATE = 45 #seconds
last_poll = 0
READ_USERS_RATE = 60 #minutes
last_read_users = 0

#config variables
printer_MAC = "00:04:48:10:7E:36"
save_dir = "../../instaprinter-photos/"
debug = False

printer_queue = Queue()

def check_feed(user):
    post = InstagramPost()
    ret  = post.poll_feed(user)
    if ret and post.is_new(user.last_id):
        user.last_id = post.id
        post.download_post()
        printer_queue.put(post)
        user.write()

def sys_call(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p.wait()
    out = p.communicate()
    return out

def send_to_printer(sourcefile):
   try:
        #connecting to printer
        sys_call(["rfkill", "unblock", "bluetooth"])
        sys_call(["rfcomm", "unbind", "/dev/rfcomm0", printer_MAC])
        sys_call(["rfcomm", "bind", "/dev/rfcomm0", printer_MAC])
        #print image
        out, error = sys_call(["ussp-push", "/dev/rfcomm0",  sourcefile , "destfile.jpg"])
        if out.decode("utf-8").find("Error") != -1 or error.decode("utf-8").find("Error") != -1:
             print("[ Error ] Unable to transfer file to printer")
   except OSError:
        print("[ Error ] Unable to execute bluetooth print")

def print_queue():
    while printer_queue.qsize() > 0:
        #create image
        post = printer_queue.get()
        img = InstagramTheme.renderTheme(post)
        #check save location
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        #save file
        filename = save_dir + post.id + ".jpg"
        img.save(filename, 'JPEG')
        #print file
        if debug:
            img.show()
        else:
            send_to_printer(filename)



print("Starting instaprinter Daemon")
while True:
    #read a list of users who use this printer
    #the list maybe updated from a http server so check periodically
    if (time.time() - last_read_users) / 60 > READ_USERS_RATE:
        print("Reading user list")
        users = User.read()
        last_read_users = time.time()

    #check our user's feeds to see if they have posted anything new
    if (time.time() - last_poll)  > POLL_RATE:
        print("polling {0} users".format(len(users)))
        for user in users:
            print("     -polling {0}".format(user.username))
            t = threading.Thread(target=check_feed, args=(user,))
            t.start()
        last_poll = time.time()

    #print anything queued up
    if printer_queue.qsize() > 0:
        print("printing {0} posts".format(printer_queue.qsize()))
        print_queue()
    time.sleep(5)
