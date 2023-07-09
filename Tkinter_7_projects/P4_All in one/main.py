#SIGNUP/LOGIN
from tkinter import *
from fnc import *
from dashboard import *

root=Tk()
root.geometry("900x700")
root.config(bg="black")

frame1=LabelFrame(root,text="ABOUT ME",font="lucida 15 bold",width=300,bg="Light blue",relief=GROOVE,bd=6)
frame1.propagate(0)
frame1.pack(side=LEFT,fill=Y,padx=5,pady=5)

# mypic=PhotoImage(file="P4_All in one\my_pic.png")
# Label(frame1,image=mypic).pack(padx=10,pady=10)

greetings="Hello!!"
frame2=LabelFrame(root,text=f"{greetings}",font="lucida 15 bold",width=300,height=300,bg="Light blue",relief=GROOVE,bd=6)
frame2.propagate(FALSE)
frame2.place(x=450,y=250)

LVAR=StringVar()        #label
SELECTED=StringVar()    #radiobtn
RVAL=None

def check(event):
    global RVAL

    rbtn=event.widget
    RVAL=rbtn["text"]

def submit():

    username=un.get()
    un.set("")
    password=pwd.get()
    pwd.set("")

    if RVAL=="Signup":
        update=signUp(username,password)   # can directly pass text var value...    need to pass un & pwd
        LVAR.set(update)

    elif RVAL=="Login":
        print(username,password)
        update=login(username,password)
        LVAR.set(update)
        if update=="Succuesfully logged in":
            root.destroy()
            window=Tk()
            dash_board(window)

    else:
        LVAR.set("Please select signup or login")

LVAR.set("Welcome please enroll")
list=["UserName","Password"]
list2=["Signup","Login"]
SELECTED.set(None)

un=StringVar()
pwd=StringVar()
var=[un,pwd]

for x in range(len(list)):
    r=Radiobutton(frame2,text=list2[x],font="lucida 15 bold",bg="Light blue",variable=SELECTED,value=list2[x])
    r.grid(row=0,column=x+2)
    r.bind("<Button-1>",check)

    Label(frame2,text=list[x],font="lucida 15 bold",bg="Light blue").grid(row=x+1,column=2,padx=10,pady=10)

    entry=Entry(frame2,font="lucida 15 bold",textvariable=var[x])
    entry.grid(row=x+1,column=3,padx=10,pady=10)

    if x==0:
        Label(frame2,textvariable=LVAR,font="lucida 15 bold",bg="Light blue").grid(row=5,column=2,columnspan=2,pady=5)


Button(frame2,text="Submit",font="lucida 15 bold",command=submit).grid(row=4,column=2,columnspan=2,pady=5)

root.mainloop()