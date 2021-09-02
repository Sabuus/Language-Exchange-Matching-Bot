import psycopg2
from Utils import HOST, DB, USER, PASS, SCHEMA

class QueryExecutor:
    # Idea is we plan to use the same table in multiple places
    TABLE = {"USER": "USERS"}
    COLUMNS =   {
                    "ALL": "*",
                    "ID": "id",
                    "NAME": "name",
                    "TIMEZONE": "timezone",
                    "LANG": "lang",
                    "START": "startTime",
                    "END": "endTime",
                }

    def connect(self):
        con = psycopg2.connect(host=HOST, database=DB, user=USER, password=PASS)
        return con

    def executeInitQuery(self, sql):

        con, cur = self.createConnection()
        
        cur.execute("BEGIN")
        existenceQuery = "select to_regclass(%s)"
        cur.execute(existenceQuery, ['{}.{}'.format(SCHEMA, self.TABLE["USER"])])

        exists = bool(cur.fetchone()[0])

        con.commit()

        if(exists):
            return

        cur.execute("BEGIN")
        cur.execute(sql)

        con.commit()

        self.exitConnection(con, cur)


    def executeQuery(self, sql):
        con, cur = self.createConnection()

        cur.execute("BEGIN")
        cur.execute(sql)

        queryResults = cur.fetchall()

        con.commit()

        self.exitConnection(con, cur)

        return queryResults


    def createConnection(self):
        con = self.connect()
        cur = con.cursor()
        return con, cur


    def exitConnection(self, con, cur):
        cur.close()
        con.close()

    def insertUser(self, userInput):
        # Really want to make this line smaller via mapper, so it's easier to read
        iterableInput = {"name": userInput.user, "timezone":"temp", "lang": userInput.languageSelected, "startTime": userInput.startTime, "endTime": userInput.endTime}
        sql = self.createInsertStatement(self.TABLE['USER'], iterableInput)

        # Only returns 1 user, so no reason to return the entire array
        return self.executeQuery(sql)[0]
    

    def createInsertStatement(self, table, userInput):
        columns = ','.join(str(v) for v in list(userInput))
        values = ','.join("'" + str(v) + "'" for v in list(userInput.values()))

        sqlStatement = "INSERT INTO {} ({}) VALUES ({}) returning *".format(table, columns, values)

        return sqlStatement


    def findUsersWithinTimeRange(self, timeRange):
        # Messy, need to think of a better way to do this
        columnsToUse = [self.COLUMNS["ID"]]
        sql = self.createSelectStatement(columnsToUse, self.TABLE["USER"])

        # left off here, not working properly
        sql += " WHERE startTime >= '{}' AND startTime <= '{}' AND endTime <= '{}' AND endTime >= '{}'".format(timeRange[0], timeRange[1], timeRange[0], timeRange[1])

        # print(sql)

        return self.executeQuery(sql)

    def getAllUsers(self):
        sql = self.createSelectStatement(self.COLUMNS['ALL'], self.TABLE['USER'])

        return self.executeQuery(sql)


    def createSelectStatement(self, columns, table, valuesToCheck = None):
        sql = "SELECT {} FROM {}".format(','.join(columns), table)

        if valuesToCheck is not None:
            sql += " WHERE "
            checkStatements = []

            for key in list(valuesToCheck):
                checkStatements.append("{}='{}'".format(key, valuesToCheck[key]))
            sql += ' AND '.join(checkStatements)
        
        return sql
