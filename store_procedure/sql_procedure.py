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
            print('Mysql connection stablished')
        except :
            print(sys.exc_info()[0],"occured.")

    def sql_connection_close(self):
        try:
            if self.connection.is_connected():
                    self.mycursor.close()
                    self.connection.close()
                    print("MySQL connection is closed")
        except :
            print(sys.exc_info()[0],"occured.")

    def check_db_sql_qurey(self):
        try:
            self.sql_cursor_start()
            self.mycursor.execute("select database();")
            r = self.mycursor.fetchall()
            print('connected data base:',r)

        except :
            print(sys.exc_info()[0],"occured.")
        # finally:
        #     self.sql_connection_close()

    def call_procedure_check_balance(self,userid,name):
        try:
            self.sql_cursor_start()
            qurey = "CALL spCheck_amount(%s,%s);"
            var = (name,userid)
            self.mycursor.execute(qurey,var)
            r = self.mycursor.fetchall()
            print("User name and amount is :",r,"respectively")
        except:
            print(sys.exc_info()[0], "occured.")
        finally:
            self.sql_connection_close()

    def call_procedure_spWithdraw_ammount(self,user_id,bank_account_id,amount_1):
        try:
            # retriving amount in account to perform check & print message
            self.sql_cursor_start()
            #checking if user is active or not
            qurey = "SELECT bank_account.`is user active` from bank_account where bank_account.`user id`=%s;"
            var = user_id
            self.mycursor.execute(qurey,var)
            r1 = self.mycursor.fetchall()
            if r1[0][0]==0:
                raise ("User is inactive unable to do transaction")
            qurey = "SELECT amount FROM bank_account where `user id`=%s;"
            var = (user_id,)
            self.mycursor.execute(qurey,var)
            r = self.mycursor.fetchall()
            print(type(r[0][0]), "respectively")
            if ((r[0][0]-amount_1)<5000):
                raise (f"Insufficient balance in account to withdraw {amount_1} amount")
            else:
                qurey = "CALL spWithdraw_ammount(%s,%s,%s);"
                var = (user_id,bank_account_id,amount_1)
                self.mycursor.execute(qurey, var)
                self.connection.commit()
                print(self.mycursor.rowcount, "record inserted.")


        except:
            print(sys.exc_info()[0], "occured.")
        finally:
            self.sql_connection_close()

    def call_procedure_transaction(self,user_id,strtdate,enddate):
        try:

            self.sql_cursor_start()

            qurey = "CALL spTransactionCheck(%s,%s,%s);"
            var = (user_id,strtdate,enddate)
            self.mycursor.execute(qurey,var)
            r = self.mycursor.fetchall()
            print(f"Following are the transaction between {strtdate} and {enddate}:")
            print("User ID,DATE,Amount")
            for i in range(len(r)):
                print(r[i])

        except:
            print(sys.exc_info()[0], "occured.")
        finally:
            self.sql_connection_close()
    def Insert_user_record(self,user_name,userDOB,userEmail):
        try:
            self.sql_cursor_start()
            qurey = "INSERT INTO user (`user name`, `user DOB`,`user email` ) VALUES (%s,%s,%s);"
            var = (user_name,userDOB,userEmail)
            self.mycursor.execute(qurey,var)
            self.connection.commit()
            print(self.mycursor.rowcount, "record inserted.")
        except:
            print(sys.exc_info()[0], "occured.")
        finally:
            self.sql_connection_close()

sql_obj = class_sql_procedure()
"""
uncomment any function to initial it. I have used trigger to do many internal functions those trigger are share in following data

"""
# sql_obj.check_db_sql_qurey()
# sql_obj.call_procedure_check_balance(1,'sarad')
# sql_obj.call_procedure_spWithdraw_ammount(1,1,20)
# sql_obj.call_procedure_transaction(1,'2022-05-05','2022-09-05')


# sql_obj.Insert_user_record('ritika','1993-03-28','ritika@abc')