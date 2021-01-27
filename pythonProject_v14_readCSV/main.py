import mysql.connector
import csv

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin123",
    db="db_TEST"
)
mycursor = mydb.cursor()
# mycursor.execute("CREATE TABLE customers (customerid INT AUTO_INCREMENT PRIMARY KEY,firstname TEXT,lastname TEXT,companyname TEXT,billingaddress1 TEXT,billingaddress2 TEXT,city TEXT,state TEXT,postalcode TEXT,country TEXT,phonenumber TEXT,emailaddress TEXT,createddate TEXT)")

csv_data = csv.reader(file('customer.csv'), delimiter=',')
count = 0
for row in csv_data:
    if count == 0:
        count +=1
    else:
        mycursor.execute("INSERT INTO customers(customerid,firstname,lastname,companyname,billingaddress1,billingaddress2,city,state,postalcode,country,phonenumber,emailaddress,createddate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",row)
        count += 1
        print(row)
print "Done"

# mycursor.execute("SELECT * FROM customers")
#
# myresult = mycursor.fetchall()
#
# for x in myresult:
#   print(x)



