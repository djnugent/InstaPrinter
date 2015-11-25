import threading
import time
from queue import Queue
from instauser import User
from instarender import InstagramTheme
from instaparser import InstagramPost

POLL_RATE = 5 #seconds
last_poll = 0
READ_USERS_RATE = 20 #minutes
last_read_users = 0

printer_queue = Queue()

def check_feed(user):
    post = InstagramPost()
    ret  = post.poll_feed(user)
    if ret and post.is_new(user.last_id):
        user.last_id = post.id
        post.download_post()
        printer_queue.put(post)
        user.write()

def print_queue():
    while printer_queue.qsize() > 0:
        post = printer_queue.get()
        img = InstagramTheme.renderTheme(post)
        img.show()


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
