from tkinter import *
from tkinter import messagebox
import random
import datetime
import pytz

WORKING_HRS=9
WORKING_DAYS=7
STARTING_TIME=9

BTN_LIST=[] #(btn,position)
days={0:"",1:"Monday",2:"Tuesday",3:"Wednesday",4:"Thursday",5:"Friday",6:"Saturday",7:"Sunday"}

DEMO_CHECK=False
DEMO_COUNT=[]
FIXED_DEMO_COUNT=[]   #should pass it to sales team

FIXED_CLASS_COUNT=[]  #contains pointer
CLASS_COUNT=[]
NEW_TIME=False

root=Tk()
root.resizable(False,False)
root.config(bg="orange")
#frame to store btns
f1=LabelFrame(root,text="Time Table",relief=GROOVE,bd=6,padx=10,pady=10)
f1.grid(row=0,column=0,padx=10,pady=10)

#frame for radio btns
f2=LabelFrame(root,text="none",relief=GROOVE,bd=6)
f2.grid(row=1,column=0)
f3=LabelFrame(root,text="Parents_Screen",relief=GROOVE,bd=6)
f3.grid(row=0,column=2,sticky="n",padx=10,pady=10)

def default_class():
    temp_list=[]
    for x in range(10):
        a=random.randint(1,126)
        while a%18==0 and a not in temp_list and a+1 not in temp_list:
            a=random.randint(1,126)
        temp_list.append(a)
        temp_list.append(a+1)
    for x,y in BTN_LIST:
        if y in temp_list:
            temp_list.remove(y)
            x.config(bg="red",state=DISABLED)
            FIXED_CLASS_COUNT.append(x)
        if y ==[]:
            break

def submit():
    global FIXED_DEMO_COUNT,DEMO_COUNT
    r=radio.get()

    if r == "demo":
        if DEMO_CHECK:
            a=messagebox.askyesno("Confirmation","do you want to save your changes")
            print(a)
            if a==False:
                for x in DEMO_COUNT:
                    x.config(bg="white")
                DEMO_COUNT=[]
                print(DEMO_COUNT)
            else:
                FIXED_DEMO_COUNT=FIXED_DEMO_COUNT+DEMO_COUNT
                DEMO_COUNT=[]
    elif r == "reschedule":
        ans=messagebox.askyesno("Confirmation","do you want to save your changes")
        print(ans)
        if ans==False:
            CLASS_COUNT[-4].config(bg="RED",state=DISABLED)
            CLASS_COUNT[-3].config(bg="RED",state=DISABLED)
            CLASS_COUNT[-2].config(bg="white",state=NORMAL)
            CLASS_COUNT[-1].config(bg="white",state=NORMAL)
            CLASS_COUNT.clear()

def adjacent_btn(x):
    x1=y1=x2=y2=0
    temp=None
    for a,b in BTN_LIST:
        if a==x:
            temp=b
            x1,y1=a,b
        elif b-1==temp:
            x2,y2=a,b
    return x1,y1,x2,y2

def adjacent_pointer(y0):
    x1 = y1 = x2 = y2 = 0
    for x,y in BTN_LIST:
        if y==y0:
            x1,y1=x,y
        elif y-1==y0:
            x2,y2=x,y
    return x1, y1, x2, y2

def fnc(event):
    global DEMO_CHECK,NEW_TIME
    r=radio.get()
    a = event.widget

    x1,y1,x2,y2=adjacent_btn(a)

    if x1 not in FIXED_CLASS_COUNT:
        if r=="demo" and x1 not in DEMO_COUNT :
            DEMO_CHECK=True             #To make sure btns are clicked
            x1.config(bg="light green")
            x2.config(bg="light green")
            DEMO_COUNT.append(x1)
            DEMO_COUNT.append(x2)
        elif r=="reschedule" and NEW_TIME:
            x1, y1, x2, y2 = adjacent_btn(a)
            x1.config(bg="light blue", state=DISABLED)
            x2.config(bg="light blue", state=DISABLED)
            messagebox.showinfo("Updating parents","Will turn to red if parents accept")
            CLASS_COUNT.append(x1)
            CLASS_COUNT.append(x2)
            NEW_TIME = False
            submit()

    else:
        if r == "reschedule":
            messagebox.showinfo("Class","you are about to reschedule this class, please Select the new class time")
            x1, y1, x2, y2=adjacent_btn(a)
            x1.config(bg="white",state=NORMAL)
            x2.config(bg="white",state=NORMAL)
            CLASS_COUNT.append(x1)
            CLASS_COUNT.append(x2)
            NEW_TIME=True

def update_lstbox(data):
    lst_box.delete(0,END)

    # Add toppings to listbox
    for item in data:
        lst_box.insert(END, item)

def fillout(event):
    Type_Zone.delete(0,END)
    Type_Zone.insert(0, lst_box.get(ANCHOR))

def search(event):
    value=Type_Zone.get()
    data=[]
    if value=="":
        data=time_zone
    else:
        for x in time_zone:
            if value.upper() in x:
                data.append(x)
    update_lstbox(data)

def notify_mentor():

    day_value=Type_Day.get()
    day_time=Type_Time.get()

    dic={"21":1,"22":3,"23":5,"0":7,"1":9,"2":11,"3":13,"4":15,"5":17}
    days = {"Monday":0,"Tuesday":18,"Wednesday":36,"Thursday":54,"Friday":72,"Saturday":90,"Sunday":108}
    #hr cannot be less then 9 and =orgreater then 18
    hr,min=day_time.split(":")
    if day_value in days:
        if hr in dic:
            y0 = dic[hr]+days[day_value]
            if min=="30":
                y0+=1
    x1, y1, x2, y2 = adjacent_pointer(y0)
    if x1 in FIXED_CLASS_COUNT or x2 in FIXED_CLASS_COUNT:
        messagebox.showerror("Apologize","Mentor already have class at this time")

    else:
        response = messagebox.askyesno("Class Reschedule request on mentor screen",
                                       f"parents want to reschedule class on {day_value} at {day_time} \n Are you available?")
        if response:
            x1.config(bg="RED",state=DISABLED)
            x2.config(bg="RED",state=DISABLED)
            FIXED_CLASS_COUNT.append(x1)
            FIXED_CLASS_COUNT.append(x2)
        else:
            messagebox.showerror("Apologize", "Mentor already have class at this time")
    Type_Day.delete(0, END)
    Type_Time.delete(0, END)
    Type_Zone.delete(0, END)



"""
def convert_datetime_timezone(dt, tz1, tz2):
    tz1 = pytz.timezone(tz1)
    tz2 = pytz.timezone(tz2)

    dt = datetime.datetime.strptime(dt,"%Y-%m-%d %H:%M:%S")
    dt = tz1.localize(dt)
    dt = dt.astimezone(tz2)
    dt = dt.strftime("%Y-%m-%d %H:%M:%S")

    return dt

#convert_datetime_timezone("2017-05-13 14:56:32", "Europe/Berlin", "PST8PDT")
#'2017-05-13 05:56:32'

#convert_datetime_timezone("2017-05-13 14:56:32", "Europe/Berlin", "UTC")
#'2017-05-13 12:56:32'
"""
for x in range(WORKING_DAYS+1):
    Label(f1, text=days[x]).grid(row=0,column=x)

t=21
for x in range(1,(WORKING_HRS*2)+1):
    if x%2!=0:
        if t==24:
            t=00
        Label(f1, text=f"{t}:00").grid(row=x,column=0)
        print(f"{t}:00", end=",")
        t+=1

count=1
for x in range(1,WORKING_DAYS+1):
    for y in range(1,(WORKING_HRS*2)+1):
        b=Button(f1,width=10)
        b.grid(row=y,column=x)
        b.bind("<Button-1>",fnc)
        BTN_LIST.append((b,count))
        count+=1

#Radio Btns
radio=StringVar()
radio.set(None)
demo=Radiobutton(f2,text="DEMO",font="Lucida 10 bold",variable=radio,value="demo")
demo.pack(side="left")
reschedule=Radiobutton(f2,text="RESCHEDULE",font="Lucida 10 bold",variable=radio,value="reschedule")
reschedule.pack(side="left")

Button(f2,text="Submit",command=submit).pack()

#parents
Label(f3,text="Please enter above details to reschedule ").grid(row=5,column=0,columnspan=2)

Label(f3,text="Type Time: ").grid(row=1,column=0,pady=5)
Label(f3,text="Type Day: ").grid(row=0,column=0,pady=5)
Label(f3,text="Select Time horizon: ").grid(row=2,column=0,pady=5)

Type_Day=Entry(f3,font="lucida 10 bold")
Type_Day.grid(row=0,column=1)
Type_Time=Entry(f3,font="lucida 10 bold")
Type_Time.grid(row=1,column=1)
Type_Zone=Entry(f3,font="lucida 10 bold")
Type_Zone.grid(row=2,column=1)

lst_box=Listbox(f3,height=3)
lst_box.grid(row=3,column=1)

Button(f3,text="Reschedule",command=notify_mentor).grid(row=3,columnspan=1)

time_zone=["UK","IST","PST","CAD","EST"]
update_lstbox(time_zone)

lst_box.bind("<<ListboxSelect>>",fillout)
Type_Zone.bind("<KeyRelease>",search)

default_class()
root.mainloop()