from tkinter import *
from tkinter import ttk
import sqlite3
import time
from collections import *
import random
from tkinter import messagebox
root = Tk()

name = StringVar()
phone = StringVar()
address = StringVar()
conn = sqlite3.connect("bus.db")
c = conn.cursor()
#c.execute("DROP TABLE DRIVER")
#c.execute("DROP TABLE CUSTOMER")
driverd = '''CREATE TABLE IF NOT EXISTS DRIVER(
   NAME text,
   PHONE text,
   ADDRESS text,
   BTYPE text,
   ORG_NAME text,
   CAPACITY INTEGER,
   STARTING text,
   ENDING text,
   PRICE INTEGER,
   DTIME_H INTEGER,
   DTIME_M INTEGER,
   ATIME_H INTEGER,
   ATIME_M INTEGER,
   DDAY INT,
   DMONTH text,
   DYEAR INT
);'''
customerdb = '''CREATE TABLE IF NOT EXISTS CUSTOMER(
   NAME text,
   CSDID INTEGER,
   SEATS INTEGER,
   PRICE INTEGER,
   TID INTEGER,
   DDID INTEGER
);'''
c.execute(driverd)
c.execute(customerdb)
c.execute('SELECT * FROM CUSTOMER')
print(c.fetchall())
def startbar():
	bar = ttk.Progressbar(root, orient = HORIZONTAL, length = 300, mode = 'determinate')
	bar.pack()
	for x in range(5):
		bar['value'] +=20
		root.update_idletasks()
		time.sleep(1)
	bar.stop()
	root.destroy()
	intermediate()

def cding(ask,idn):
		bar = ttk.Progressbar(ask, orient = HORIZONTAL, length = 300, mode = 'determinate')
		bar.pack()
		for x in range(3):
			bar['value'] +=33
			ask.update_idletasks()
			time.sleep(1)
		bar.stop()
		check = int(idn.get())
		print(type(check))
		c.execute('SELECT * FROM CUSTOMER WHERE TID = ?',(check,))
		tdetail = c.fetchall()
		if(len(tdetail)==0):
			messagebox.showerror("Invalid", "THIS ID DOES NOT EXIST, PLEASE RECHECK OR CONTACT US!")
			ask.destroy()
		else:
			c.execute('SELECT * FROM DRIVER WHERE rowid = ?',(tdetail[0][5]+1,))
			ddetail = c.fetchall()
			detailed = "Customer's Name "+str(tdetail[0][0])+"\n Seats Booked: "+str(tdetail[0][1])+"\n Driver's Name: "+str(ddetail[0][0])+"\n Driver's Phone Number: "+str(ddetail[0][1])+"\n TYPE: "+str(ddetail[0][3])+"\n Providers: "+str(ddetail[0][4])+"\n From: "+str(ddetail[0][6])+"\n Destination: "+str(ddetail[0][7])+"\n Arrival Time:"+str(ddetail[0][9])+":"+str(ddetail[0][10])+"\n Reaching Time: "+str(ddetail[0][11])+":"+str(ddetail[0][12])+"\n Journey Date: "+str(ddetail[0][13])+" "+str(ddetail[0][14])+" "+str(ddetail[0][15])+"\n PRICE :"+str(tdetail[0][3])
			messagebox.showinfo("Customer Detail",detailed)
			ask.destroy()


def Checkdetails():
	ask = Tk()
	ask.geometry("200x90")
	ask.title("ID ENTRY SCREEN")
	Label(ask,text = "Enter your Ticket ID ").pack()
	idn = Entry(ask)
	idn.pack()
	Button(ask, text = "CONFIRM",command = lambda:cding(ask,idn)).pack()
	

def verify(ping,hehe,v,cusname,seats):
	c.execute('SELECT * FROM DRIVER')
	table =(c.fetchall())
	v = int(v)
	if(table[v][5]-int(seats.get()) < 0):
		hehe.destroy()
		ping.destroy()
		messagebox.showerror("Insufficient Seats", "Not Enough Seats Available\nKindly check later.")
	else:
		c.execute('''UPDATE DRIVER SET CAPACITY = CAPACITY - ? WHERE rowid = ?''',(int(seats.get()), v+1))
		print(seats.get())
		conn.commit()
		c.execute('SELECT * FROM DRIVER')
		print(c.fetchall())
		nono = random.randint(10000,100000)
		naam = str(cusname.get())
		booked_seats = int(seats.get())
		c.execute("""INSERT INTO CUSTOMER VALUES (?, ?, ?, ?, ?, ?)""",(naam,nono,booked_seats,int(table[v][8])*booked_seats,nono, v))
		conn.commit()
		bar = ttk.Progressbar(hehe, orient = HORIZONTAL, length = 300, mode = 'determinate')
		bar.grid(row =3 ,column =0)
		for x in range(3):
			bar['value'] +=33
			hehe.update_idletasks()
			time.sleep(1)
		bar.stop()
		messagebox.showinfo("Ticket Confirmed", "Your Ticket Has Been Successfully Booked!\n Your Ticket ID is:"+str(nono)+"\n Keep your ID with you\nHappy Journey!")
		hehe.destroy()
		ping.destroy()


def confirmbook(ping,v):
	final = Toplevel()
	final.title("Details Screen")
	Label(final, text = "Your Name:").grid(row = 0, column =0)
	custname = StringVar()
	cusname = Entry(final, textvariable = custname)
	cusname.grid(row=0, column = 1)
	Label(final, text = "Seats:").grid(row =1,column=0)
	seats = Entry(final)
	seats.grid(row =1, column =1)	
	Button(final, text = "BOOK NOW!", command = lambda: verify(ping,final,v,custname,seats)).grid(row =2,column =1)



def search(ping,sourcev,targetv,availtypesv,datev,monthv,yearv):
	bar = ttk.Progressbar(ping, orient = HORIZONTAL, length = 300, mode = 'determinate')
	bar.grid(row =11 ,column =0)
	for x in range(3):
		bar['value'] +=33
		ping.update_idletasks()
		time.sleep(1)
	bar.stop()
	ping.destroy()
	hehe = Tk()
	hehe.title("Select Your Ride")
	hehe.geometry("1200x300")
	h1 = sourcev.get()
	h2 = targetv.get()
	h3 = availtypesv.get()
	h4 = int(datev.get())
	h5 = monthv.get()
	h6 = int(yearv.get())
	if h3 == 'ALL':
		c.execute("""SELECT * From DRIVER WHERE STARTING = ? AND ENDING = ? AND DDAY = ? AND DMONTH = ? AND DYEAR =? """,(h1,h2,h4,h5,h6))
	else:
		c.execute("""SELECT * From DRIVER WHERE STARTING = ? AND ENDING = ? AND DDAY = ? AND DMONTH = ? AND DYEAR =? AND BTYPE = ?""",(h1,h2,h4,h5,h6,h3))
	found = c.fetchall()
	Label(hehe, text = "COMPANY NAME",font=('Helvetica', 18, 'bold')).grid(row = 0, column= 0)
	Label(hehe, text = "FROM",font=('Helvetica', 18, 'bold')).grid(row = 0, column= 1)
	Label(hehe, text = "DESTINATION",font=('Helvetica', 18, 'bold')).grid(row = 0, column= 2)
	Label(hehe, text = "TYPE",font=('Helvetica', 18, 'bold')).grid(row = 0, column= 3)
	Label(hehe, text = "ARRIVAL",font=('Helvetica', 18, 'bold')).grid(row = 0, column= 4)
	Label(hehe, text = "DEPARTURE",font=('Helvetica', 18, 'bold')).grid(row = 0, column= 5)
	Label(hehe, text = "PRICE",font=('Helvetica', 18, 'bold')).grid(row = 0, column= 6)
	Label(hehe, text = "AVAIL. SEATS",font=('Helvetica', 18, 'bold')).grid(row = 0, column= 7)
	Label(hehe, text = "BOOK",font = ('Helvetica', 18, 'bold')).grid(row = 0, column= 8)

	if(len(found)==0):
		hehe.destroy()
		messagebox.showerror("Not Found!", "No Drivers Availabe at this Date and Location")
		
	v = StringVar(hehe, "0") 
  	
	for i in range(0,len(found)):
		Label(hehe, text = found[i][4],font=('Helvetica', 18)).grid(row = i+1, column =0)
		Label(hehe, text = found[i][6],font=('Helvetica', 18)).grid(row = i+1, column =1)
		Label(hehe, text = found[i][7],font=('Helvetica', 18)).grid(row = i+1, column =2)
		Label(hehe, text = found[i][3],font=('Helvetica', 18)).grid(row = i+1, column =3)
		Label(hehe, text = str(found[i][9])+":"+str(found[i][10]),font=('Helvetica', 18)).grid(row = i+1, column =4)
		Label(hehe, text = str(found[i][11])+":"+str(found[i][12]),font=('Helvetica', 18)).grid(row = i+1, column =5)
		Label(hehe, text = found[i][8],font=('Helvetica', 18)).grid(row = i+1, column =6)
		Label(hehe, text = found[i][5],font=('Helvetica', 18)).grid(row = i+1, column =7)
		Radiobutton(hehe, variable = v,value = i).grid(row = i+1, column = 8)

	Button(hehe, text = "CONFIRM", command  = lambda: confirmbook(hehe,v.get())).grid(row = len(found)+1, column = 8)



def intermediate():
	root = Tk()
	root.title("Selection Screen")
	root.geometry("450x535")
	second = Label(root, text = "Select Your Choice", bg = 'black', fg = 'green', font=("Times New Roman", 24))
	second.config(height = 7, width = 7)
	second.pack(fill = X, ipady =20)
	driver = Button(root, text = "Add A Driver", bg = 'Red', fg = 'green', font = 18,command=adddriver)
	driver.config(height = 1, width = 1)
	driver.pack(fill = X, ipady = 20)
	passenger = Button(root,text = "Book A Ride", bg = 'green',fg='red', font = 18,command = customer)
	passenger.config(height = 1, width = 1)
	passenger.pack(fill = X, ipady = 20)
	ticketd = Button(root,text = "Check Ticket Details", bg = 'red',fg='blue', font = 18,command = Checkdetails)
	ticketd.config(height = 1, width = 1)
	ticketd.pack(fill = X, ipady = 20)

def customer():
	ping = Toplevel()
	ping.geometry("450x600")
	ping.title("Search A Ride")
	heading = Label(ping,text ="Ajay Booking Services",bg = "green",fg ='blue', font=("Times New Roman", 24))
	heading.grid(row = 0, columnspan = 4, sticky = E)
	bus2 = PhotoImage(file = "bus.png")
	bus2 = bus2.subsample(2,2)
	photo = Label(ping,image = bus2)
	c.execute('SELECT * FROM DRIVER')
	table =(c.fetchall())
	sourcev = StringVar(ping)
	targetv = StringVar(ping)
	availtypesv = StringVar(ping)
	datev = StringVar(ping)
	monthv = StringVar(ping)
	yearv = StringVar(ping)
	sourcelist =['Select Starting Point']
	targetlist= ['Select Destination Point']
	availtypes = ['ALL']
	cdate = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
	cmonth = ['January', 'February', 'March', 'April', 'May', 'June', 'July','August', 'September', 'October', 'November', 'December']
	cyear = ['2020', '2021']
	for drivers in table:
		source = drivers[6].upper()
		sourcelist.append(source)
		target = drivers[7].upper()
		targetlist.append(target)
		typo = drivers[3].upper()
		availtypes.append(typo)
	res = list(OrderedDict.fromkeys(sourcelist))
	sourcelist = res
	res = list(OrderedDict.fromkeys(targetlist))
	targetlist = res
	res = list(OrderedDict.fromkeys(availtypes))
	availtypes = res
	# print(sourcelist)
	# print(targetlist)
	sourcev.set(sourcelist[0])
	targetv.set(targetlist[0])
	availtypesv.set(availtypes[0])
	datev.set(cdate[0])
	monthv.set(cmonth[0])
	yearv.set(cyear[0])
	photo.grid(row = 2, columnspan = 4)
	Label(ping, text = "Source").grid(row = 4, column =0)
	cussource =  OptionMenu(ping, sourcev, *sourcelist)
	cussource.grid(row = 4, column = 1)
	Label(ping, text = "Destination").grid(row = 5, column = 0)
	cusdestination = OptionMenu(ping, targetv, *targetlist)
	cusdestination.grid(row = 5, column = 1)
	Label(ping, text = "Bus Type").grid(row = 6, column =0)
	custype = OptionMenu(ping, availtypesv, *availtypes)
	custype.grid(row = 6, column = 1)
	Label(ping, text = "Journey Date").grid(row =7, column =0)
	date = OptionMenu(ping, datev, *cdate)
	date.grid(row = 7, column =1)
	Label(ping, text = "Month").grid(row =8, column =0)
	month = OptionMenu(ping, monthv, *cmonth)
	month.grid(row = 8, column=1)
	Label(ping, text = "Year").grid(row =9, column =0)
	year = OptionMenu(ping, yearv, *cyear)
	year.grid(row = 9, column=1)
	searchb = Button(ping, text = "Search", command = lambda: search(ping,sourcev,targetv,availtypesv,datev,monthv,yearv))
	searchb.grid(row = 10, column = 1)


def printer(ping,namebox,addressbox,phonebox,ogname,bustypes,capacity_box,from_box,destination,pricet,time_h,time_m,atime_h,atime_m,ddate,dmonth,dyear):
	if not((len(bustypes.get())) and len(ogname.get()) and len(capacity_box.get()) and len(from_box.get()) and len(destination.get()) and len(pricet.get()) and len(time_h.get()) and len(time_m.get()) and len(atime_h.get()) and len(atime_m.get())):
		messagebox.showerror("Details Not Filled", "Please Check All the Boxes and enter correct details")
		ping.destroy()
	elif str(from_box.get()).upper() == str(destination.get()):
		messagebox.showerror("CANNOT BE SAME", "BOTH THE DESTINATIONS CANNOT BE SAME")
		ping.destroy()

	else:
		enterdate = [(str(namebox.get()).upper(),str(phonebox.get()).upper(),str(addressbox.get()).upper(),str(bustypes.get()).upper(),str(ogname.get()).upper(),int(capacity_box.get()),str(from_box.get()).upper(),str(destination.get()).upper(),int(pricet.get()),int(time_h.get()),str(time_m.get()),int(atime_h.get()),str(atime_m.get()),int(ddate.get()),str(dmonth.get()),str(dyear.get()))]
		print(enterdate)
		c.executemany("INSERT INTO DRIVER VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",enterdate)
		conn.commit()
		messagebox.showinfo("Succesful", "Your Details have Been Added By Us!")
		ping.destroy()




def driverinfo(ping,namebox,addressbox,phonebox):
	Label(ping, text= "Bus Type").grid(row = 8, column = 0)
	typec = StringVar()
	bustypes = ttk.Combobox(ping, width = 27, textvariable = typec) 
	bustypes['values'] = ['AC','NON-AC','SLEEPER','CHAIRCAR']
	bustypes.grid(row = 8, column = 1)
	bustypes.current(0)
	bustype = bustypes.get()
	Label(ping, text = "Organization Name").grid(row =9, column =0)
	onname = StringVar()
	ogname = Entry(ping, textvariable=onname)
	ogname.grid(row=9, column =1)
	Label(ping, text = "Bus Capacity").grid(row = 10, column = 0)
	tempbox = StringVar()
	capacity_box = Entry(ping, textvariable = tempbox)
	capacity_box.grid(row = 10, column = 1)
	Label(ping, text = "From:").grid(row = 11, column =0)
	from_box = Entry(ping)
	from_box.grid(row = 11, column = 1)
	Label(ping, text = "Destination:").grid(row = 12, column =0)
	destination = Entry(ping)
	destination.grid(row = 12,column =1)
	Label(ping, text = "Per Ticket Price:").grid(row = 13, column =0)
	pricet = Entry(ping)
	pricet.grid(row = 13, column =1)
	htime = StringVar()
	mtime= StringVar()
	ahtime = StringVar()
	amtime= StringVar()
	Label(ping,text = "Departure Time(HOURS):").grid(row = 14,column=0)
	time_h = ttk.Combobox(ping, width = 27, textvariable = htime) 
	time_h.grid(row = 14, column = 1)
	time_h['values']=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','00']
	Label(ping,text = "Departure Time(Minutes):").grid(row = 15,column=0)
	time_m = ttk.Combobox(ping, width = 27, textvariable = mtime) 
	time_m.grid(row = 15, column = 1)
	time_m['values']=['00','15','30','45']
	Label(ping,text = "Arrival Time(HOURS):").grid(row = 16,column=0)
	atime_h = ttk.Combobox(ping, width = 27, textvariable = ahtime) 
	atime_h.grid(row = 16, column = 1)
	atime_h['values']=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','00']
	Label(ping,text = "Arrival Time(Minutes):").grid(row = 17,column=0)
	atime_m = ttk.Combobox(ping, width = 27, textvariable = amtime) 
	atime_m.grid(row = 17, column = 1)
	atime_m['values']=['00','15','30','45']
	Label(ping,text = "Departure Date(Month): ").grid(row = 18, column =0)
	dmonth = ttk.Combobox(ping, width = 27)
	dmonth['values'] = ['January', 'February', 'March', 'April', 'May', 'June', 'July','August', 'September', 'October', 'November', 'December']
	dmonth.grid(row = 18, column = 1)
	month = str(dmonth.get())
	Label(ping,text = "Year").grid(row = 19, column =0)
	dyear = ttk.Combobox(ping, width = 27) 
	dyear['values'] = ['2020', '2021']
	dyear.grid(row =19, column = 1)
	Label(ping, text = 'Date').grid(row =20,column = 0)
	ddate = ttk.Combobox(ping, width = 27) 
	ddate['values'] = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
	ddate.grid(row =20, column =1 )
	testb = Button(ping, text = "Confirm!", command = lambda :printer(ping,namebox,addressbox,phonebox,ogname,bustypes,capacity_box,from_box,destination,pricet,time_h,time_m,atime_h,atime_m,ddate,dmonth,dyear))
	testb.grid(row = 21, column =1)


def resizedriver(ping,namebox,addressbox,phonebox):
	if  (len(addressbox.get()) and len(phonebox.get()) and len(namebox.get())):
		ping.geometry("400x750")
		driverinfo(ping,namebox,addressbox,phonebox)
	else:
		messagebox.showerror("Details Not Filled", "Please Check All the Boxes and enter correct details and Ensure A 10 Digit Phone Number.")
		ping.destroy()

if __name__=="__main__": 
	
	root.title("Ajay Booking Services")
	root.geometry("900x475")
	welcome_label = Label(root, text = "Welcome To Ajay Services",bg = "green",fg ='blue', font=("Times New Roman", 24))
	welcome_label.pack(fill = X, ipady = 30)
	bus = PhotoImage(file = "bus.png")
	bus = bus.subsample(2,2)
	photo = Label(root,image = bus)
	photo.pack(ipadx = 10, ipady = 0)
	cont_button = Button(root,text = "Continue", font = 10, bg ="white", command = startbar)
	cont_button.pack(ipadx = 15)
	
	def adddriver():
		ping = Toplevel()
		ping.title("Adding A Bus Operator")
		ping.geometry("400x450")
		heading = Label(ping,text ="Ajay Booking Services",bg = "green",fg ='blue', font=("Times New Roman", 24))
		heading.grid(row = 0, columnspan = 4, stick = NSEW)
		bus2 = PhotoImage(file = "bus.png")
		bus2 = bus2.subsample(2,2)
		photo = Label(ping,image = bus2)
		photo.grid(row = 2, columnspan = 4)
		namelabel = Label(ping, text = "Driver Name:").grid(row = 3, column =0)
		namebox = Entry(ping,textvariable = name)
		namebox.grid(row =3, column = 1)
		phonelabel = Label(ping, text= "Contact Number:").grid(row = 4, column=0)
		phonebox = Entry(ping, textvariable = phone)
		phonebox.grid(row = 4, column =1)
		addresslabel = Label(ping, text = "Address").grid(row =5, column = 0)
		addressbox = Entry(ping, textvariable = address)
		addressbox.grid(row =5, column = 1)
		proceedbutton = Button(ping,text = "Proceed",command =lambda: resizedriver(ping,namebox,addressbox,phonebox)).grid(row= 6, column = 1)





	mainloop()
