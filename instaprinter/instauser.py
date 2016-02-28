import shelve
import os
db_file = os.path.realpath(__file__).replace("instauser.py","users.db")
db = shelve.open(db_file)

class User():
    users = []
    @classmethod
    def read(cls):
        keys = db.keys()
        cls.users = []
        for key in keys:
            cls.users.append(db[key])
        return cls.users
    @classmethod
    def add(cls,username,access_token):
        user = cls(username,access_token)
        cls.users.append(user)
        db[user.username] = user
        db.sync()
    @classmethod
    def remove(cls, username):
        try:
            #remove locally
            for user in cls.users:
                if user.username == username:
                    cls.users.remove(user)
            #remove from db
            del db[username]
            db.sync()
            return True
        except KeyError:
            return False

    def __init__(self, username, access_token):
        self.username = username
        self.access_token = access_token
        self.last_id = ""

    def write(self):
        db[self.username] = self
        db.sync()

    def __str__(self):
        return "User: {}, Token: {}, Last Photo ID: {}".format(self.username ,self.access_token,self.last_id)

if __name__ == "__main__":
    #run a CLI for managing users

    exit = False
    while not exit:
        try:
            cli = input('>>>').split()
            if len(cli) > 0:
                cmd = cli[0]
                if cmd == "help":
                    print("User management for InstaPrinter")
                    print("    add [user] [access_token]         #adds a new user")
                    print("    remove [user]                     #removes an existing user")
                    print("    reset [user]                      #reset a user's last_id")
                    print("    list                              #lists all users")
                    print("    exit                              #exit CLI")

                elif cmd == "list":
                    print("Users:")
                    users = User.read()
                    for u in users:
                        print(u)

                elif cmd == "add":
                    if len(cli) != 3:
                        print("invalid usage: add [user] [access_token]")
                    else:
                        username = cli[1]
                        access_token = cli[2]

                        if len(access_token) != 51:
                            print("add failed: invalid access_token length")
                            continue

                        ret = User.add(username,access_token)
                        print("added user: {} access_token: {}".format(cli[1],cli[2]))

                elif cmd == "remove":
                    if len(cli) != 2:
                        print("invalid usage: remove [user]")
                    else:
                        username = cli[1]
                        ret = User.remove(username)
                        if ret:
                            print("removed user: {}".format(username))
                        else:
                            print("remove failed: user does not exist")

                elif cmd == "reset":
                    if len(cli) != 2:
                        print("invalid usage: reset [user]")
                    else:
                        username = cli[1]

                        ret = False
                        users = User.read()
                        for u in users:
                            if u.username == username:
                                u.last_id = None
                                u.write()
                                ret = True
                                break

                        if ret:
                            print("reset user: {}".format(username))
                        else:
                            print("reset failed: user does not exist")

                elif cmd == "exit":
                    exit = True

                else:
                    print("invalid command: enter 'help' to see commands")

        except KeyboardInterrupt:
            exit = True



'''


    #add users
    print("adding 2 users")
    User.add("snoopdog","This is a key")
    User.add("obama","This is a key also")
    users = User.read()
    print_users(users)

    #remove a user
    print("removing a user")
    User.remove("obama")
    users = User.read()
    print_users(users)

    #modify a user
    print("modifying a user")
    user = users[0]
    user.access_token = "new key"
    user.write()
    users = User.read()
    print_users(users)
'''
