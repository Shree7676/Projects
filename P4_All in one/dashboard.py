from tkinter import *
from tkinter import filedialog, ttk, messagebox
import os
import pandas as pd
import csv

class dash_board:
    def __init__(self,a) -> None:
        self.r=a    # a >> root=Tk()
        self.r.geometry("800x520")
        self.r.title("Dashboard")
        self.r.resizable(0,0)

        self.col_name=["Sl.No","File","Action"]
        self.file_Details={}

        # btn:filepath
        self.download={}
        self.open={}

        self.butn=Button(text="Upload",font="lucida 15 bold",command=self.open_).place(x=375,y=450)

        for x in range(3):
            Label(self.r,text=self.col_name[x],font="lucida 15 bold").grid(row=0,column=x,padx=20)

    def open_(self):
        filedetail=filedialog.askopenfile(filetypes=(("CSV files","*.csv"),("Excel files", "*.xlsx")))
        filename=os.path.basename(filedetail.name)
        filepath=filedetail.name
        self.file_Details[filename]=filepath
        self.update()

    def down(self,event):
        btn=event.widget
        file_path = filedialog.asksaveasfilename(defaultextension='.xlsx')
        if file_path:
            # Open the xlsx file
            if "xlsx" in self.download[btn]:
                with open(self.download[btn], 'rb') as file:
                    file_contents = file.read()

                # Save the file to the specified location
                with open(file_path, 'wb') as new_file:
                    new_file.write(file_contents)
            else:
                with open(self.download[btn], 'r') as file:
                    reader = csv.reader(file)
                    data = [row for row in reader]

                # Save the csv file to the specified location
                with open(file_path[:-5] + ".csv", 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(data)
            messagebox.showinfo("Successfully Saved","Your file has been saved")

    def opening(self,event):
        btn=event.widget

        new_window=Toplevel(self.r)
        new_window.title("Data")

        frame1=Frame(new_window)
        frame1.pack(padx=20,pady=20,fill=BOTH)

        my_tree=ttk.Treeview(frame1)

        path=self.open[btn]
        df=pd.read_csv(path)
        my_tree["column"]=list(df.columns)
        my_tree["show"]="headings"

        for column in my_tree["column"]:
            my_tree.heading(column,text=column)

        df_rows = df.to_numpy().tolist()
        for row in df_rows:
            my_tree.insert("","end",values=row)

        my_tree.pack()


    def update(self):
        count=1
        for x in self.file_Details:
            Label(text=count,pady=5,font="lucida 10 bold").grid(row=count,column=0,padx=20,pady=10)
            Label(text=x,pady=5,font="lucida 10 bold").grid(row=count,column=1,padx=20,pady=10)
            
            btn1=Button(text="Download",pady=5)
            btn1.grid(row=count,column=2,padx=20,pady=10)
            btn1.bind("<Button-1>",self.down)
            self.download[btn1]=self.file_Details[x]

            btn2=Button(text="Open",pady=5)
            btn2.grid(row=count,column=3,padx=20,pady=10)
            btn2.bind("<Button-1>",self.opening)
            self.open[btn2]=self.file_Details[x]

            count+=1


if __name__=="__main__":
    root=Tk()
    p=dash_board(root)
    root.mainloop()
