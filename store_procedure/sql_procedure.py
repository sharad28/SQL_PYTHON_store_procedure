import sys

import mysql.connector
from mysql.connector import Error


class class_sql_procedure:

    def sql_cursor_start(self):
        try:
            self.connection = mysql.connector.connect(host='localhost',
                                                 database='emp',
                                                 user='root',
                                                 password='1234')
            self.mycursor = self.connection.cursor()

        except :
            print("oops",sys.exc_info()[0],"occured.")

    def sql_connection_close(self):
        try:
            if self.connection.is_connected():
                    self.mycursor.close()
                    self.connection.close()
                    print("MySQL connection is closed")
        except :
            print("oops",sys.exc_info()[0],"occured.")





