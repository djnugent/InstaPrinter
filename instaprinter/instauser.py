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
            return True
        except KeyError:
            return False

    def __init__(self, username, access_token):
        self.username = username
        self.access_token = access_token
        self.last_id = ""

    def write(self):
        db[self.username] = user
        db.sync()

    def __str__(self):
        return str(self.__dict__)

if __name__ == "__main__":

    def print_users(users):
        for u in users:
            print(u)

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
