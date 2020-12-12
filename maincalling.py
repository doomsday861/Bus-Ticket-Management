from tkinter import *
from tkinter import ttk
import sqlite3
import time
from tkinter import messagebox
root = Tk()

name = StringVar()
phone = StringVar()
address = StringVar()
conn = sqlite3.connect("bus.db")
c = conn.cursor()
# c.execute("DROP TABLE DRIVER")
# driverd = '''CREATE TABLE DRIVER(
#    NAME text,
#    PHONE text,
#    ADDRESS text,
#    BTYPE text,
#    ORG_NAME text,
#    CAPACITY INT,
#    STARTING text,
#    ENDING text,
#    PRICE INT,
#    DTIME_H INT,
#    DTIME_M INT,
#    ATIME_H INT,
#    ATIME_M INT
# )'''
# c.execute(driverd)
c.execute('SELECT * FROM DRIVER')
print(c.fetchall())
def startbar():
	bar = ttk.Progressbar(root, orient = HORIZONTAL, length = 300, mode = 'determinate')
	bar.pack()
	# for x in range(5):
	# 	bar['value'] +=20
	# 	root.update_idletasks()
	# 	time.sleep(1)
	bar.stop()
	root.destroy()
	intermediate()





def intermediate():
	root = Tk()
	root.title("Selection Screen")
	root.geometry("450x440")
	second = Label(root, text = "Select Your Choice", bg = 'black', fg = 'green', font=("Times New Roman", 24))
	second.config(height = 7, width = 7)
	second.pack(fill = X, ipady =20)
	driver = Button(root, text = "Add A Driver", bg = 'Red', fg = 'green', font = 18,command=adddriver)
	driver.config(height = 1, width = 1)
	driver.pack(fill = X, ipady = 20)
	passenger = Button(root,text = "Book A Ride", bg = 'green',fg='red', font = 18)
	passenger.config(height = 1, width = 1)
	passenger.pack(fill = X, ipady = 20)

def printer(ping,namebox,addressbox,phonebox,ogname,bustypes,capacity_box,from_box,destination,pricet,time_h,time_m,atime_h,atime_m):
	if not((len(bustypes.get())) and len(ogname.get()) and len(capacity_box.get()) and len(from_box.get()) and len(destination.get()) and len(pricet.get()) and len(time_h.get()) and len(time_m.get()) and len(atime_h.get()) and len(atime_m.get())):
		messagebox.showerror("Details Not Filled", "Please Check All the Boxes and enter correct details")
		ping.destroy()
	else:
		enterdate = [(str(namebox.get()),str(phonebox.get()),str(addressbox.get()),str(bustypes.get()),str(ogname.get()),int(capacity_box.get()),str(from_box.get()),str(destination.get()),int(pricet.get()),int(time_h.get()),int(time_m.get()),int(atime_h.get()),int(atime_m.get())),(str(namebox.get()),str(phonebox.get()),str(addressbox.get()),str(bustypes.get()),str(ogname.get()),int(capacity_box.get()),str(from_box.get()),str(destination.get()),int(pricet.get()),int(time_h.get()),int(time_m.get()),int(atime_h.get()),int(atime_m.get()))]
		print(enterdate)
		c.executemany("INSERT INTO DRIVER VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",enterdate)
		c
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
	testb = Button(ping, text = "OK", command = lambda :printer(ping,namebox,addressbox,phonebox,ogname,bustypes,capacity_box,from_box,destination,pricet,time_h,time_m,atime_h,atime_m))
	testb.grid(row = 19, column =0)


def resizedriver(ping,namebox,addressbox,phonebox):
	if  (len(addressbox.get()) and len(phonebox.get()) and len(namebox.get())):
		ping.geometry("400x700")
		driverinfo(ping,namebox,addressbox,phonebox)
	else:
		messagebox.showerror("Details Not Filled", "Please Check All the Boxes and enter correct details")
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
		heading.grid(row = 0, columnspan = 4)
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
