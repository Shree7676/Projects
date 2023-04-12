from project_files import app
from flask import render_template, request
from project_files import models

DF_COLLECTION=[]
MERGED_DF=[]

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/yt_decode', methods=["GET", "POST"])
def yt_decode():
    global DF_COLLECTION,MERGED_DF

    if request.method == "POST":
        data = request.form['content']
        list_data=data.split(',')
        df,DF_COLLECTION,MERGED_DF=models.get_yt_df(list_data)
    return render_template('result.html', tables=[MERGED_DF.to_html(classes='table-users header', header="true")], titles=MERGED_DF.columns.values)

