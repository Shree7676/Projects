from project_files import app
from project_files.models import Application
from flask import render_template
from flask import Response
import tkinter as tk

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tkinter')
def tkinter_app():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
    return Response(status=200)