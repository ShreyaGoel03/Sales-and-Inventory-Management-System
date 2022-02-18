import mysql.connector #Library to connect to database
import pandas as pd
import hashlib #Libraries for encrypting the password
import getpass 
from passlib.hash import sha256_crypt 

#Class for connecting to the Database 
class Database:
    def __init__(self,host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    #Connecting to the database   
    def connect_db(self): 
        mydb = mysql.connector.connect(host=self.host, user=self.user, passwd = self.password, database=self.database)
        return mydb

#Class for login as admin or salesman
class Login:
	def __init__(self, db, username, password, user):
		self.db = db
		self.username = username
		self.password = password
		self.user = user

	#Verifying the credentials for login
	def authenticate(self):
		conn = self.db.connect_db()  
		mycursor = conn.cursor()      
		mycursor.execute("SELECT name,password FROM login WHERE username = %s AND user_type = %s",(self.username, self.user))
		if_exist_username = mycursor.fetchall()
		if len(if_exist_username) != 0 and sha256_crypt.verify(self.password,if_exist_username[0][1]):
			print("\nLogin Successful!")
			print("Welcome",if_exist_username[0][0])
			return 1
		else:
			print("No such user exists!")
			return 0

#Class for signing up as admin or salesman
class Signup:
	def __init__(self,db,name,username,password, user):
		self.db = db
		self.username = username
		self.password = password
		self.name = name
		self.user = user

	#Registering the user either as admin or salesman
	def register(self):
		conn = self.db.connect_db()  
		mycursor = conn.cursor()
		passwd = self.password 
		hash = sha256_crypt.hash(passwd)

		try:
			mycursor.execute("INSERT into login values(%s,%s,%s,%s)",(self.username,self.name,hash,self.user))
			conn.commit()
			return 0
		except mysql.connector.Error as err:
		    return 1

#Class to View the contents of Inventory
class Inventory:
	def __init__(self,db):
		self.db = db
	#Viewing the contents of the inventory
	def display(self):
		conn = self.db.connect_db()
		mycursor = conn.cursor()
		mycursor.execute("SELECT * FROM items")	#Displaying all the contents of the items table
		myresult = mycursor.fetchall()
		df =  pd.DataFrame(myresult,columns=['Item_ID','Item_Name','Item_Quantity','Item_Price'])
		print("\nInventory List\n",df)

#Class to generate the report
class Generate_Report:
	def __init__(self,db):
		self.db = db

	def generate_report():
		pass

#Class to generate the Inventory Report by inheriting the Generate_Report class 
class Generate_Inventory_Report(Generate_Report):
	def __init__(self,db):
		self.db = db

	#Generating the inventory report within a given time span
	def generate_report(self):
		conn = self.db.connect_db()
		mycursor = conn.cursor()
		start_date = input("Enter start date in YYYY-MM-DD format ")
		end_date = input("Enter End date in YYYY-MM-DD format ")
		#Displaying the inventory turnover for a specific period of time
		mycursor.execute('SELECT * from inventory_report where date between %s and %s',(start_date, end_date))
		items = mycursor.fetchall()
		df =  pd.DataFrame(items,columns=['Report_ID','Operation_Performed','Item_ID','Item_Name','Item_Quantity','Date'])
		print("\nInventory Report List\n",df)

#Class to generate the Sales report by inheriting the Generate_Report class 
class Generate_Sales_Report(Generate_Report):
	def __init__(self,db):
		self.db = db

	def generate_report(self):#Generating the sales report 
		conn = self.db.connect_db()
		mycursor = conn.cursor()
		start_date = input("Enter start date in YYYY-MM-DD format ")
		end_date = input("Enter End date in YYYY-MM-DD format ")
		#Displaying the sales report for the specified period of time
		mycursor.execute('SELECT * from sales_report where date between %s and %s',(start_date, end_date))
		sales = mycursor.fetchall()	
		df1 =  pd.DataFrame(sales,columns=['S_ID','Customer_Name','Total_Amount','Date'])
		if (df1.empty):
			print("NO Current Sales Record Available!")
		else:
			print("\nSales Report\n",df1)

#Class to place orders of items in the inventory
class Place_Orders:  

    def __init__(self,db):
        self.db = db

    def place_order(self):  #Ordering an item which is less in stock            
        conn = self.db.connect_db()
        mycursor = conn.cursor()      
        while(1):               
            id = int(input("\nEnter item id "))
            name = input("Enter item name ")
            qty = int(input("Enter item quantity "))
            #Insert the pending items into the pending_items table 
            mycursor.execute("SELECT * from items where id = %s",(id,))
            item_list = mycursor.fetchall()            
            if(len(item_list) != 0):
                mycursor.execute("SELECT * from pending_items where order_done=0 and item_id = %s",(id,))
                items = mycursor.fetchall()
                if(len(items) == 0):	                    	    
                    mycursor.execute("INSERT into pending_items(item_id,item_name,item_quantity) values(%s,%s,%s)",(id,name,qty,))
                    conn.commit()                
                else:
                    mycursor.execute("UPDATE pending_items set item_quantity=item_quantity + %s where item_id=%s",(qty,id,))
                    conn.commit()
                print("Order Placed Successfully!")
            else:
                print("Item not in Inventory. Add item to the Inventory first.")
            cont = input("Order more items? Enter y/n ")
            if cont == "n":
                break

#Changing the status of the orders being delivered
class Delivered_Orders:
	def __init__(self,db):
		self.db = db

	def change_delivery_status(self): #Marking the order as done when delivered
		conn = self.db.connect_db()
		mycursor = conn.cursor()      
		while(1):
			mycursor.execute("SELECT * from pending_items")
			pending = mycursor.fetchall()
			if len(pending) != 0:
			    id = int(input("Enter Order ID "))			        
			    #Updating the order as done in the pending_items table
			    query = "UPDATE pending_items SET order_done=1 WHERE order_id=%s" 
			    mycursor.execute(query,(id,))
			    conn.commit()
			    print("Order marked as done")      		    		                  		        
			    cont = input("Change Delivery Status for any order? Enter y/n ")
			    if cont == 'n':
			        break 
			else:
				print("There are no pending orders")
				break

#Class for Viewing the orders placed
class View_Pending_Orders:

    def __init__(self,db):
        self.db = db

    def view_order(self): # Viewing all the pending orders which are not yet delivered 
        conn = self.db.connect_db()
        mycursor = conn.cursor()      
        #Fetching all the orders which are not delivered from the pending_items table
        mycursor.execute('SELECT order_id,item_id, item_name, item_quantity from pending_items where order_done=0')
        pending_items = mycursor.fetchall()
        df =  pd.DataFrame(pending_items,columns=['ORDER_ID','Item_ID','Item_Name','Item_Quantity'])
        if (df.empty):
        	print("\nNo Pending Orders")
        else:
        	print("\nPending Orders List\n",df)		
                
#Class for cancelling the placed orders
class Cancel_Orders:
	def __init__(self,db):
		self.db = db

	def cancel_order(self): #Cancelling the placed order 
		conn = self.db.connect_db()
		mycursor = conn.cursor() 
		order_id = int(input("Enter order id of the order to be cancelled "))
		#Selecting and cancelling the orders
		mycursor.execute("SELECT * from pending_items where order_id = %s and order_done = 0",(order_id,))
		results = mycursor.fetchall()
		if(len(results) == 0):
		    print("\nThere is no pending order of given order id ")
		else:
		    mycursor.execute("DELETE from pending_items where order_id = %s",(order_id,))
		    conn.commit()
		    print("\nOrder Cancelled Successfully")

#Changing the changing the price of items
class Modify_Price:
	def __init__(self,db):
		self.db = db
	
	def change_price(self): #Changing the price of an item
		conn = self.db.connect_db()
		mycursor = conn.cursor() 
		while(1):
		    id = int(input("Enter item id "))
		    new_price = int(input("Enter new price "))
		    #Updating the price of an item with new price
		    mycursor.execute("UPDATE items set price=%s where id=%s",(new_price,id,))
		    conn.commit()
		    print("Price changed successfully!")
		    cnt = input("Change price of more items? Enter y/n ")
		    if cnt == 'n':
		        break

#Adding the new items in inventory
class Modify_items:
    def __init__(self,db):
        self.db = db

    def add_new_item(self): #Adding a new item into the inventory
        conn = self.db.connect_db()
        mycursor = conn.cursor()		
        while(1):
            id = int(input("Enter item id "))
            name = input("Enter item name ")            
            price = int(input("Enter price "))
            date = input("Enter date ")
            try:
           		#Inserting new item into the items table
           		mycursor.execute("INSERT into items values(%s,%s,%s,%s)",(id,name,0,price,))
           		conn.commit()	           
           		print("Item added in Inventory ")
           		#Adding the action of adding new item into the inventory
           		mycursor.execute("INSERT into inventory_report(operation, item_id, item_name, item_qty, date) values(%s,%s,%s,%s,%s)",("New Item Added",id,name,0,date))
           		conn.commit()
            except mysql.connector.Error as err : 
            	print("Item with this ID already Exists!")
            cnt = input("Add more items? Enter y/n ")
            if(cnt == 'n'):
            	break

#Adding the items in the inventory which has 
class Add_Items_Inventory:
	def __init__(self,db):
		self.db = db

	def add_items(self): #Adding items that are delivered into the inventory
		conn = self.db.connect_db()
		mycursor = conn.cursor(buffered=True)
		date = input("Enter the Date in YY/MM/DD format ")
		#Selecting the items that are delivered
		mycursor.execute("SELECT * from pending_items where order_done = 1")
		ids = mycursor.fetchall()
		conn.commit()
		for id1 in ids:
			#Inserting the transactions of adding items into the inventory_report
			mycursor.execute("INSERT into inventory_report(operation,item_id,item_name,item_qty,date) values(%s,%s,%s,%s,%s)",("Added Item",id1[1],id1[2],id1[3],date))				
			#Updating the quantity of the delivered items in the items table
			mycursor.execute("UPDATE items SET quantity=quantity + %s where id=%s" ,(id1[3],id1[1],))								
			mycursor.execute("DELETE FROM pending_items where item_id=%s",(id1[1],))
			conn.commit()
		print("Items Added Successfully!\n")

#Displaying items present less in stcok i.e. less than the threshold value
class Stock_Alert:
	def __init__(self,db):
		self.db = db

	def send_less_stock_alert(self):#Displaying the items which are less in stock
		threshold_value = 10
		conn = self.db.connect_db()
		mycursor = conn.cursor(buffered=True)
		#Selecting the items whose quantity is less than the threshold value
		mycursor.execute("SELECT id,name,quantity from items where quantity <= %s",(threshold_value,))
		data = mycursor.fetchall()
		df = pd.DataFrame(data,columns = ['Item_ID','Item_Name','Item_Quantity'])
		if(df.empty):
			print("No item with less stock is available\n")
		else:
			print("Items with less stock available are\n",df)
			
#Deleting items from the inventory which are sold to the customers
class Delete_Items_Inventory:
	def __init__(self,db):
		self.db = db

	def delete_items(self): #Updating the stocks after a sale has been made 
		conn = self.db.connect_db()
		mycursor = conn.cursor(buffered=True)
		#Selecting the items bought by the customers
		mycursor.execute("SELECT i_id,quantity,date from items_bought")
		ids = mycursor.fetchall()
		for id1 in ids:
			#Updating the quantitites in the items table
			mycursor.execute("SELECT name from items where id=%s",(id1[0],))
			value1 = mycursor.fetchone()[0]
			#Inserting the transaction of selling items into the inventory report
			mycursor.execute("INSERT into inventory_report(operation,item_id,item_name,item_qty,date) values(%s,%s,%s,%s,%s)",("Sold Item",id1[0],value1,id1[1],id1[2]))
			#Updating the stock in the items table
			mycursor.execute("UPDATE items SET quantity=quantity - %s where id=%s" ,(id1[1],id1[0],))
			mycursor.execute("DELETE FROM items_bought where i_id=%s",(id1[0],))
			conn.commit()
		print("Item Stock Updated!\n")

    
class Generate_Bills:
	def __init__(self,db):
		self.db = db

	#Generating bill for a customer
	def generate_bill(self):
		conn = self.db.connect_db()
		mycursor = conn.cursor()
		#Entering the details of the customer
		cust_name = input("Enter the Customer Name ")
		date = input("Enter the Date in YY/MM/DD format")
		df = pd.DataFrame(columns = ['Item_Name','Item_Quantity','Item_Price','Total_Price'])
		total_price=0
		while(1):#Listing the items bought by the customer
			i_id = int(input("Enter item id "))
			name = input("Enter item name ")
			quantity = int(input("Enter quantity "))
			mycursor.execute("SELECT price from items where id = %s",(i_id,))
			price = mycursor.fetchone()[0]
			total_price = price*quantity
			df = df.append({'Item_Name':name,'Item_Quantity':quantity,'Item_Price':price,'Total_Price':total_price},ignore_index = True)
			total_price = 0
			#Inserting the items bought by the customer into the items_bought table
			mycursor.execute("INSERT into items_bought(i_id,quantity,date) values(%s,%s,%s)",(i_id,quantity,date))
			conn.commit()
			cont = input("Continue? Type y/n ")
			if cont == 'n':
				break
		#Inserting the transactions performed into the sales_report table
		mycursor.execute("INSERT into sales_report(cust_name,total_amount,date) values(%s,%s,%s)",(cust_name,df['Total_Price'].sum(axis = 0, skipna = True),date))
		conn.commit()
		print("\n\nGenerated Bill is: ")
		print("Customer Name ",cust_name)
		print(df)
		print("Total Amount is : ",df['Total_Price'].sum(axis = 0, skipna = True))
		
#Function for order of execution
def main():
	while(1):
		db = Database("localhost", "root", "Shreyasql@7", "sims") 
		print("Welcome To SIMS!! Who are you? \n1. Admin \t 2.Salesman \t 3.Exit")
		choice_1 = int(input("Enter 1 for Admin, 2 for Salesman, 3 for Exit "))
		ans = 'n'
		if choice_1 == 3:
			print("Thank You!")
			break

		elif choice_1 == 1 or choice_1 == 2:
			choice_2 = int(input("\nEnter 1 for Login, 2 for Signup, 3 for Exit "))
			if choice_2 == 3:
			 	break

			if choice_2 == 2:
				while(1):
					print("\nEnter Details for Signup")
					name = str(input("Name: "))
					username = str(input("Username: "))
					password = getpass.getpass(prompt="Password: ")
					user = choice_1
					
					sign = Signup(db,name,username,password,user)
					ans = sign.register()
					if ans == 0:
						print("User Registered Successfully!")
						print("Please Login Now")
						ans = str(input("Do you want to Login now? Enter y/n"))
						break
					else:
						print("\nSame User Already Exists!")
						print("Enter Details Again")

			if choice_2 == 1 or ans == 'y':
				while(1):
					print("\nEnter Login Details")
					username = str(input("Username: "))
					password = getpass.getpass(prompt="Password: ")
					user = choice_1
					login_user = Login(db,username,password,user)
					ans = login_user.authenticate()
					if ans == 0:
						print("Enter Again!")
					else:
						if choice_1 == 1:
							while(1):
							    print("\nChoose the action:\n1.Manage Orders \t 2.Add New Items \t 3.Change price of Item \t 4.View Inventory \t 5.Exit")
							    op_choice = int(input("Enter 1 to Manage Orders, 2 to Add New Item, 3 to Change Price of Item, 4 to View Inventory, 5 to Exit "))
							    if op_choice == 1:
							        print("\n1.Place new order \t 2.View Pending orders \t 3.Cancel Order \t 4.Exit")
							        order_choice = int(input("Enter 1 to Place New Order, 2 to View Pending Orders, 3 to Cancel Pending Orders, 4 to Exit "))
							        if order_choice == 1:
							            admin = Place_Orders(db)
							            admin.place_order()
							        elif order_choice == 2:
							            monitor = View_Pending_Orders(db)
							            monitor.view_order()	           
							            alter = input("\nChange Delivery Status for any order? Enter y/n ")
							            if alter == 'y':
							            	status = Delivered_Orders(db)
							            	status.change_delivery_status()                                                
							        elif order_choice == 3:
							            cancel = Cancel_Orders(db)
							            cancel.cancel_order()   

							    elif op_choice == 2:
							        modify = Modify_items(db)
							        modify.add_new_item() 
							    elif op_choice == 3:
							        modify = Modify_Price(db)
							        modify.change_price()   
							    elif op_choice == 4:
							        inventory = Inventory(db)
							        inventory.display()
							        ir = input("Generate Inventory report? Enter y/n ")
							        if ir == 'y':
							        	inventory = Generate_Inventory_Report(db)
							        	inventory.generate_report()
							    elif op_choice == 5:
							    	break
							    else:
							    	print("Wrong Choice!")

						elif choice_1 == 2:
							while(1):
								print("\nChoose the action:\n 1. View Inventory \t 2. Generate Bills \t 3.Update Inventory \t 4.Generate Sales Report \t 5.Exit")
								op_choice = int(input("Enter 1 to View Inventory, 2 to Generate Bills , 3 to Update Inventory, 4 to Generate Sales Report, 5 to Exit "))
								
								if op_choice == 1:
									inventory = Inventory(db)
									inventory.display()
									ir = input("Generate Inventory report? Enter y/n ")
									if ir == 'y':
									    inventory = Generate_Inventory_Report(db)
									    inventory.generate_report()

								elif op_choice == 2:
									salesman = Generate_Bills(db)
									salesman.generate_bill()

								elif op_choice == 3:
									
									print("\n1.Add Items \t 2.Delete Items and Send Less Stock Alert")
									choice_3 = int(input("Enter 1 for Add Items, 2 for Delete Items and Send Less Stock Alert "))
									if choice_3 == 1:
										add = Add_Items_Inventory(db)
										add.add_items()

									elif choice_3 == 2:
										delete = Delete_Items_Inventory(db)
										delete.delete_items()
										ls = str(input("\nDo you want to check less stock? Enter y/n "))
										if ls=='y':
											less_stock = Stock_Alert(db)
											less_stock.send_less_stock_alert()

								elif op_choice == 4:
									sales_report = Generate_Sales_Report(db)
									sales_report.generate_report()

								elif op_choice == 5:
									break

								else:
									print("Wrong Choice!")
						
						elif choice_1 == 3:
							break 
						break

			elif ans == 'n':
				print("\nOkay! Thank you!\n")

			else:
				print("\nWrong Choice\n")
		else:
			print("\nWrong Choice! Please Enter Again\n")

if __name__ == "__main__":
	main()