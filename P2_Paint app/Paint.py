from tkinter import *
from tkinter import colorchooser,messagebox
from tkinter.filedialog import asksaveasfilename
import PIL.ImageGrab as ImageGrab

class Paint():
    def __init__(self,a):
        self.r=a    # a >> root=Tk()
        self.r.geometry("800x520")
        self.r.title("Paint")
        self.r.config(bg="red")
        self.r.resizable(0,0)

        self.pen_colour="black"
        self.eraser_color="white"

        #adding widget to tkinter
        self.color_frame=LabelFrame(self.r,text="Color",font="Arial 15",bd=5,relief=RIDGE,bg="white")
        self.color_frame.place(x=0,y=0,width=70,height=185)

        colors=["black","red","blue","violet","brown","green","orange","light blue","light green","yellow","indigo","white"]
        i=j=0
        for colour in colors:
            Button(self.color_frame,bg=colour,bd=2,relief=RIDGE,width=3,command=lambda col=colour :self.select_color(col)).grid(row=i,column=j)
            i+=1
            if i==len(colors)/2:
                i=0
                j+=1

        self.eraser_button=Button(self.r,text="ERASER",bd=4,bg="white",command=self.eraser,width=8,relief=RIDGE)
        self.eraser_button.place(x=0,y=187)

        self.clear_button=Button(self.r,text="CLEAR",bd=4,bg="white",command=lambda : self.canvas.delete("all"),width=8,relief=RIDGE)
        self.clear_button.place(x=0,y=217)

        self.save_button=Button(self.r,text="SAVE",bd=4,bg="white",command=self.save_,width=8,relief=RIDGE)
        self.save_button.place(x=0,y=247)

        self.canvas_button=Button(self.r,text="CANVAS",bd=4,bg="white",command=self.canvas_color,width=8,relief=RIDGE)
        self.canvas_button.place(x=0,y=277)



        self.pen_size_frame=LabelFrame(self.r,text="size",bd=5,bg="white",font="Arial 15",relief=RIDGE)
        self.pen_size_frame.place(x=0,y=310,height=200,width=70)

        self.pen_size=Scale(self.pen_size_frame,orient=VERTICAL,from_=50 ,to=0,length=160)
        self.pen_size.set(5)
        self.pen_size.grid(row=0 , column=1,padx=10)

        self.canvas=Canvas(self.r,bg="white",bd=5,relief=GROOVE,height=500,width=700)
        self.canvas.place(x=80,y=0)
        self.canvas.bind("<B1-Motion>",self.paint)

    def paint(self,event):
        x1=(event.x-2)
        y1=(event.y-2)
        x2=(event.x+2)
        y2=(event.y+2)

        self.canvas.create_oval(x1,y1,x2,y2,fill=self.pen_colour,outline=self.pen_colour,width=self.pen_size.get())

    def select_color(self,col):
        self.pen_colour=col

    def eraser(self):
        self.pen_colour =self.eraser_color

    def canvas_color(self):
        color=colorchooser.askcolor()
        print(color[1]) #rgb>>0 hexadecimal>>1
        self.canvas.configure(background=color[1])
        self.eraser_color=color[1]

    def save_(self):
        try :
            filename=asksaveasfilename(defaultextension=".jpg")
            x=self.r.winfo_rootx()+self.canvas.winfo_x()
            y=self.r.winfo_rooty()+self.canvas.winfo_y()
            x1= x + self.canvas.winfo_width()
            y1= y + self.canvas.winfo_height()
            print(x,y,x1,y1)
            ImageGrab.grab().crop((x,y,x1,y1)).save(filename)
            messagebox.showinfo("Status",f"File Saved in + {str(filename)}")
        except:
            messagebox.showerror("Status", "we ran into an issue plz save us mighty coder")



if __name__=="__main__":
    root=Tk()
    p=Paint(root)
    root.mainloop()

