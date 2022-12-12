from tkinter import *

BTN_LIST=[]
object_list = []  # [(pointer,obj of rashi,butn)]

root = Tk()
root.title("RASHI- By Narayan Nandiyawar")
root.config(bg="light blue")
root.resizable(False,False)

class rashi:
    def __init__(self, home, frnd="frnd", enemy="enemy", normal="None", feature="feat"):
        self.home = home
        self.frnd = frnd        #should be object of class rashi
        self.enemy = enemy      #should be object of class rashi
        self.normal = normal    #should be object of class rashi
        self.feature = feature


planets = {1: ("surya", "mesh"), 2: ("chandra", "rushab"), 3: ("rahu", "mithun"),
           4: ("brahaspati", "kark"), 5: ("none5", "siha"), 6: ("budh", "kanya"),
           7: ("shani", "tula"),8:("none8","vruschik"), 9: ("ketu", "dhanu"),
           10: ("mangal", "makar"),11: ("none11", "kumba"), 12: ("shukra", "miin")}

def display(ras):
    Details = LabelFrame(root, text="Details", width=400, height=435, font=("lucida 10 bold"))
    Details.propagate(0)
    Details.grid(row=1, column=2, pady=5, padx=5)
    for x in vars(ras):
        Label(Details,text=f"{x}:\t{vars(ras)[x]}",font=("lucida 20 bold")).pack()


kundali=LabelFrame(root,text="Kundali",width=400,height=350,font=("lucida 10 bold"))
kundali.propagate(0)
kundali.grid(row=1,column=1,pady=5,padx=5,ipadx=5,ipady=5)


Label(kundali,text="\tOriginal position",font=("lucida 20 bold")).grid(row=0,column=0,columnspan=4)
#creating btn
r,c=1,2
for x in planets:
    i = rashi(x)
    b=Button(kundali,text=f"{planets[x][1]} Rashi\n{planets[x][0]} Graha\n{x}",width=15,height=5,bg="orange",font=("lucida 10 bold"),command=lambda a=i:display(a))
    if r==1 and (c==2 or c==3 or c==4):
        #print(r, c,x)
        b.grid(row=r, column=c)
        if c==4 and r==1:
            r+=1
        if c!=4:
            c += 1
    elif c==4 and r<=4:
        #print(r, c,x,"hlo")
        b.grid(row=r, column=c)
        if r==c:
            c-=1
        if r!=4:
            r+=1
    elif r==4 and c>=1:
        #print(r, c,x,"hi")
        b.grid(row=r, column=c)
        if r==4 and c==1:
            r-=1
        if c!=1:
            c -= 1
    elif c==1 and r>=1:
        #print(r, c,x)
        b.grid(row=r, column=c)
        r -= 1
    BTN_LIST.append((x,i,b))


root.mainloop()
