import pymysql
from datetime import date
import time
import os
from dotenv import load_dotenv
load_dotenv()

def getconnection():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )

def check_exists(Accno):
    mycon = getconnection()
    mycursor = mycon.cursor()
    sql = "SELECT * FROM CUSTOMER WHERE Accno = '%s'"%(Accno,)
    mycursor.execute(sql)
    mydata=mycursor.fetchall()
    if mycursor.rowcount==0:
        return False
    else:
        return True
    
def addcustomer():
    mycon = getconnection()
    mycursor = mycon.cursor()
    Name=input("Enter Customer Name: ")
    Address=input("Enter Customer Address: ")
    Telno=input("Enter Customer Telno: ")
    dop=str(date.today())
    acctype=input("Enter the Account Type (Savings/Current): ")
    amt=float(input("Enter the Initial Deposit: "))
    sql = "INSERT INTO CUSTOMER (Name,Address,Tellno,dop,acctype) VALUES ('%s','%s','%s','%s','%s')"%(Name,Address,Telno,dop,acctype)
    mycursor.execute(sql)
    mycon.commit()
    sql = "SELECT * FROM CUSTOMER"
    mycursor.execute(sql)
    mydata=mycursor.fetchall()
    accno=mydata[-1][0]
    sql = "INSERT INTO BNKTRANSACTION VALUES ('%s','%s','%s','%s','%s')"%(accno,dop,'D',amt,amt)
    mycursor.execute(sql)
    mycon.commit()
    print("Your Account Number is: ",accno)
    print("Record Inserted Successfully")
    mycon.close()

def displaycustomer():
    mycon = getconnection()
    mycursor = mycon.cursor()
    Accno=int(input("Enter Account Number:"))
    sql = "SELECT * FROM CUSTOMER WHERE Accno = '%s'"%(Accno,)
    mycursor.execute(sql)
    mydata=mycursor.fetchall()
    if mycursor.rowcount==0:
        print("Invalid Account Number!")
    else:
        print("Name: ",mydata[0][1])
        print("Address: ",mydata[0][2])
        print("Telno: ",mydata[0][3])
        print("Account Type: ",mydata[0][5])
        print("DOP: ",mydata[0][4])
    mycon.close()

def displayall():
    mycon = getconnection()
    mycursor = mycon.cursor()
    sql = "SELECT * FROM CUSTOMER"
    mycursor.execute(sql)
    mydata=mycursor.fetchall()
    if mycursor.rowcount==0:
        print("No Records Found!")
    else:
        print("%8s %15s %15s %15s %15s %15s"%("Accno","Name","Address","Telno","AccType","DOP",))
        for x in mydata:
            print("%8s %15s %15s %15s %15s %15s"%(x[0],x[1],x[2],x[3],x[5],x[4],))
    mycon.close()

def updatecustomer():
    mycon = getconnection()
    mycursor = mycon.cursor()
    Accno=int(input("Enter Account Number:"))
    if check_exists(Accno)==True:
        print("Enter 1 to edit Address")
        print("Enter 2 to edit Telno")
        ch=int(input("Enter your choice: "))
        if ch==1:
            add=input("Enter new Address: ")
            sql = "UPDATE CUSTOMER SET Address = '%s' WHERE Accno = '%s'"%(add,Accno,)
        elif ch==2:
            telno=int(input("Enter new Telno: "))
            sql = "UPDATE CUSTOMER SET Tellno = '%s' WHERE Accno = '%s'"%(telno,Accno,)
        else:
            print("Invalid Choice!")
        if ch in(1,2):
            mycursor.execute(sql)
            mycon.commit()
            print("Record Updated Successfully!")
    else:
        print("Invalid Account Number!")
    mycon.close()

def deletecustomer():
    mycon = getconnection()
    mycursor = mycon.cursor()
    accno=int(input("Enter Account Number: "))
    if check_exists(accno)==True:
        sql = "DELETE FROM CUSTOMER WHERE Accno = '%s'"%(accno,)
        sql1 = "DELETE FROM BNKTRANSACTION WHERE Accno = '%s'"%(accno,)
        mycursor.execute(sql1)
        mycursor.execute(sql)
        mycon.commit()
        print("Record Deleted Successfully!")
    else:
        print("Invalid Account Number!")
    mycon.close()


def deposit():
    mycon = getconnection()
    mycursor = mycon.cursor()
    print("Depost Option")
    dot=date.today()
    print("Today's Date: ",dot)
    accno=int(input("Enter Account Number: "))
    sql = "SELECT * FROM CUSTOMER WHERE Accno = '%s'"%(accno,)
    mycursor.execute(sql)
    mydata=mycursor.fetchall()
    if mycursor.rowcount==0:
        print("Invalid Account Number!")
    else:
        amt=float(input("Enter Amount to Deposit: "))
        sql = "SELECT * FROM BNKTRANSACTION WHERE Accno = '%s'"%(accno,)
        mycursor.execute(sql)
        mydata=mycursor.fetchall()
        bal=mydata[-1][0]
        bal=bal+amt
        sql = "INSERT INTO BNKTRANSACTION VALUES ('%s','%s','D','%s','%s')"%(accno,dot,amt,bal)
        mycursor.execute(sql)
        mycon.commit()
        print("Amount Deposited Successfully!")
        print("Current Balance: ",bal)
    mycon.close()

def withdraw():
    mycon = getconnection()
    mycursor = mycon.cursor()
    print("Withdraw Option")
    dot=date.today()
    print("Today's Date: ",dot)
    accno=int(input("Enter Account Number: "))
    sql = "SELECT * FROM CUSTOMER WHERE Accno = '%s'"%(accno,)
    mycursor.execute(sql)
    mydata=mycursor.fetchall()
    if mycursor.rowcount==0:
        print("Invalid Account Number!")
    else:
        acctype=mydata[0][5]
        amt=float(input("Enter Amount to Withdraw: "))
        sql = "SELECT * FROM BNKTRANSACTION WHERE Accno = '%s'"%(accno,)
        mycursor.execute(sql)
        mydata=mycursor.fetchall()
        bal=mydata[-1][4]
        if acctype.lower()=='savings':
            if bal - amt >= 100:
                bal=bal-amt
                sql = "INSERT INTO BNKTRANSACTION VALUES ('%s','%s','W','%s','%s')"%(accno,dot,amt,bal)
                mycursor.execute(sql)
                mycon.commit()
                print("Amount Withdrawn Successfully!")
                print("Current Balance: ",bal)
            else:
                print("Insufficient Balance! A minimum balance of 100 is required in Savings Account.")
        elif acctype.lower()=='current':  # Added current account handling
            if bal - amt >= 0:
                bal=bal-amt
                sql = "INSERT INTO BNKTRANSACTION VALUES ('%s','%s','W','%s','%s')"%(accno,dot,amt,bal)
                mycursor.execute(sql)
                mycon.commit()
                print("Amount Withdrawn Successfully!")
                print("Current Balance: ",bal)
            else:
                print("Insufficient Balance!")
        else:
            print("Unknown account type!")
    mycon.close()

def transreport():
    mycon = getconnection()
    mycursor = mycon.cursor()
    accno=int(input("Enter Account Number: "))
    sql = "SELECT * FROM BNKTRANSACTION WHERE Accno = '%s'"%(accno,)
    mycursor.execute(sql)
    mydata=mycursor.fetchall()
    if mycursor.rowcount==0:
        print("Invalid Account Number!")
    else:
        print("%8s %20s %20s %20s %15s"%("Accno","Date of Transaction","Transaction Type","Amount","Balance",))
        for x in mydata:
            print("%8s %20s %20s %20s %15s"%(x[0],x[1],x[2],x[3],x[4],))
    mycon.close()


#main program
print("\n\n")
while True:
    print("\n\nMenu")
    print("1. Add Customer")
    print("2. Delete Customer")
    print("3. Update Customer")
    print("4. Display All Customer")
    print("5. Display Customer Details")
    print("6. Transaction")
    print("7. Exit")
    ch=int(input("Enter your choice: "))
    if ch==1:
        addcustomer()
    elif ch==2:
        deletecustomer()
    elif ch==3:
        updatecustomer()
    elif ch==4:
        displayall()
    elif ch==5:
        displaycustomer()
    elif ch==6:
        while True:
            print("\n\nTransaction Menu")
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Transaction Report")
            ch1=int(input("Enter your choice: "))
            if ch1==1:
                deposit()
                break
            elif ch1==2:
                withdraw()
                break
            elif ch1==3:
                transreport()
                break
            else:
                print("Invalid Choice!")
    elif ch==7:
        print("Thank you for Using this Software!")
        break
    else:
        print("Invalid Choice! Please select a valid option.")