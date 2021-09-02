from datetime import datetime
from QueryExecutorModule import QueryExecutor

class DatabaseWrapper:
    executor = QueryExecutor()

    def register(self, userInput):
        storedUser = self.executor.insertUser(userInput)

        print("Registered")

        return storedUser


    def matchUsers(self, userData):
        userTimes = list(filter(lambda data: type(data) == datetime, userData))

        print(userTimes)

        return self.executor.findUsersWithinTimeRange(userTimes)

        
    def cancel(self, name, id):
        sql = "SELECT name FROM USERS WHERE id=%s" % id
        con, cur = self.executioner(sql)
        try:
            if cur.fetchone()[0] == name:
                self.exitConnection(con, cur)
                sql = "DELETE FROM USERS WHERE id=%s" % id
                self.exitConnection(*self.executioner(sql))
                return "Canceled"
            else:
                return "You can't cancel other's reservation"
        except TypeError:
            return "You don't have any reservation"

    
    def init(self):
        sql = "CREATE TABLE USERS (id SERIAL, name text, timezone text, lang text, startTime timestamp, endTime timestamp, isMatched boolean DEFAULT false)"

        self.executor.executeInitQuery(sql)

        print("Initialized")


    def showAllUsers(self):
        users = self.executor.getAllUsers()
        for user in users:
            print(user)

        return "Message too big, sent to console"


    def showChannels(self, g):
        s = ""
        for v in g.voice_channels:
            s += (v.name + "\n")
        return s
