from typing import Type
import psycopg2
from Utils import HOST, DB, USER, PASS

class DatabaseWrapper:
    def connect(self):
        con = psycopg2.connect(host=HOST, database=DB, user=USER, password=PASS)
        return con


    def exitConnection(self, con, cur):
        cur.close()
        con.close()


    def executioner(self, sql):
        con = self.connect()
        cur = con.cursor()
        cur.execute("BEGIN")
        cur.execute(sql)
        con.commit()
        return (con, cur)


    def checkID(self, name):
        sql = "SELECT id from USERS WHERE name='%s'" % name
        con, cur = self.executioner(sql)
        id = cur.fetchone()[0]
        self.exitConnection(con, cur)
        return id


    def register(self, userInput):
        # sql = "INSERT INTO USERS (name, timezone, lang, startTime, endTime) VALUES ('%s', %s, '%s', '%s', '%s', '%s', '%s')" % (userInput.user, 0, userInput.languageSelected, userInput.startTime, userInput.endTime)
        objectsToInsert = { "name": "'" + userInput.user + "'", "timezone":"'temp'", "lang": "'" + userInput.languageSelected + "'"}

        times = {"startTime": userInput.startTime, "endTime": userInput.endTime }

        # Convert to function
        # Need to learn how to handle the times
        sql = "INSERT INTO USERS ("
        sql += ','.join(list(objectsToInsert))
        sql += ", startTime, endTime) VALUES ("
        
        sql += ','.join(list(objectsToInsert.values()))
        sql += ", '%s', '%s')" % (times["startTime"], times["endTime"])

        self.exitConnection(*self.executioner(sql))
        print("Registered")


    
    def init(self):
        sql = "CREATE TABLE USERS (id SERIAL, name text, timezone text, lang text, startTime timestamp, endTime timestamp)"
        self.exitConnection(*self.executioner(sql))
        print("Initialized")

    

    def showAllUsers(self):
        sql = "SELECT * FROM USERS"
        con, cur = self.executioner(sql)
        rows = cur.fetchall()
        s = ""
        for r in rows:
            print(r)
        self.exitConnection(con, cur)


    def showChannels(self, g):
        s = ""
        for v in g.voice_channels:
            s += (v.name + "\n")
        return s

        
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


    