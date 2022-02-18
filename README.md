# Sales-and-Inventory-Management-System
## Overview 
<p align = "justify">
The Sales and Inventory Management System for a Departmental Store has two main components:<br/>
<b> 1. Admin</b> <br/>
<b> 2. Salesman</b> <br/>
It is a console based application with the MySQL database which has 6 tables as follows:
login, items, pending_items, items_bought, inventory_report, sales_report.<br/></p>
<br/>

## Admin Operations
<p align = "justify">
After login as Admin, the operations that are available to the admin are<br/>
<b>1. Manage Orders</b> : When the stock of any item becomes very low, the admin can order items to
the supplier so that it is available in sufficient quantity.<br/>
&nbsp;&nbsp;&nbsp;<b>1.1. Place New Order </b>: The admin can order items by giving its ID, name and quantity.<br/>
&nbsp;&nbsp;&nbsp;<b>1.2. View Pending Orders </b>: The admin can view the list of items placed before and yet to be
delivered.<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>1.2.1. Change Delivery Status </b>: Once the items are delivered, the admin can mark that
particular order as Done by giving its ID.<br/>
&nbsp;&nbsp;&nbsp;<b>1.3. Cancel Orders</b> : The admin can cancel the order which was placed and not yet delivered.<br/>
<b>2. Add New Items </b></b>: When the admin wants to add a new item to the inventory, he can add it
by mentioning the details of the item item ID, item name and item initial price.<br/>
<b>3. Change Price of Item </b>: The admin can change the price of an existing item in the inventory
by specifying the item ID and the new price.<br/>
<b>4. View Inventory </b>: The admin can view the contents of the inventory.<br/>
&nbsp;&nbsp;&nbsp;<b>4.1. Generate Inventory Report </b>: The admin can generate a full report of the inventory
turnover for a specific period by giving the start and end date.<br/></p>
<br/>

## Salesman Operations
<p align = "justify">
After login as Salesman, the operations that are available to salesman are<br/>
<b>1. View Inventory </b>: The salesman can view the contents of the inventory.<br/>
&nbsp;&nbsp;&nbsp;<b>1.1. Generate Inventory Report</b> : The salesman can generate a full report of the
inventory turnover for a specific period by giving start and end date.<br/>
<b>2. Generate Bills </b>: The Salesman can generate a bill for each Customer by entering the name
of the customer and then the ID, name, quantity of each item bought. The bill along with the
total amount to be paid by the customer is displayed.<br/>
<b>3. Update Inventory </b>: The Salesman can update the items in the Inventory.<br/>
&nbsp;&nbsp;&nbsp;<b>3.1. Add Items </b>: When the admin makes an order and the items are delivered, they
are added to the inventory by the salesman by using the Item ID from the
pending_items table.<br/>
&nbsp;&nbsp;&nbsp;<b>3.2. Delete Items </b>: The quantity of the items purchased by the customer are deleted
from the inventory to get the updated quantities by using the Item ID from the
items_bought table.<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>3.2.1. Send Less Stock Alert </b>: The salesman display all the items when the
quantity of that item in the inventory is below a threshold value.<br/>
<b>4. Generate Sales Report </b>: The Salesman can generate the sales report, which has all the
transactions done by the customers for a specific period by entering the start and end date.<br/></p>
<br/>

## Databases
The tables created and used in MySQL Databases are:<br/><br/>
<b>1. Login Table</b>:This table stores the username, name, password and the type of user whether admin or salesman. The passwords are stored in an excrypted format. The details of the user during signup is stored over here.<br/>
<p float = "center">
<img src = "https://user-images.githubusercontent.com/43794593/154765442-1a5f00dd-ca62-4879-aa2f-900fc2026481.png" width = 40% height = 40%></p>

<b>2. Items Table</b>: The item ID, name, quantity and price of the item present in the inventory is stored over here.<br/>
<p float = "center">
<img src = "https://user-images.githubusercontent.com/43794593/154765591-8b5d1fd8-5299-4bf2-b716-5409717d49c3.png" width = 40% height = 40%></p>
  
<b>3. Pending Items Table</b>:The orders of the list of items placed before and yet to be delivered are stored here.<br/>
<p float = "center">
<img src = "https://user-images.githubusercontent.com/43794593/154765600-a066f292-1c19-4026-b52b-8a4f15bb0ea4.png" width = 40% height = 40%></p>
  
<b>4. Inventory Report Table</b>:The transactions of the items(addition of a new item, adding items in stock and selling of items) that have taken place in the store is stored here to generate the inventory report. <br/>
<p float = "center">
<img src = "https://user-images.githubusercontent.com/43794593/154765617-2354f6f5-a88a-4e16-815e-37224ebb2fe1.png" width = 40% height = 40%></p>
  
<b>5.Items Bought Table</b>: The details of the items bought by the customer are stored over here which is later used to generate the bill.<br/>
<p float = "center">
<img src = "https://user-images.githubusercontent.com/43794593/154765647-e9757f83-c12d-4bc2-b663-f26bcf91f87f.png" width = 40% height = 40%></p>
  
<b>6. Sales Report Table</b>:Sales which is the total amount of the items bought by each customer are stored here. <br/>
<p float = "center">
<img src = "https://user-images.githubusercontent.com/43794593/154765676-e9dbd206-b9b4-4adb-8916-c953d7ea5d4f.png" width = 40% height = 40%></p>

