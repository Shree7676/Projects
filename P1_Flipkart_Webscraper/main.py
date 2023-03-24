from flask import Flask, render_template, request
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import logging
import requests
import pymongo

app=Flask(__name__)
FLIPKART_URL="https://www.flipkart.com/search?q="

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/review',methods=["GET","POST"])
def web_scraper():
    if request.method=="POST":
        data=request.form['content']
        search_url=FLIPKART_URL+data

        data_html=bs(urlopen(search_url).read(),'html.parser')
        data_box=data_html.find_all("div",{"class":"_1AtVbE col-12-12"})
        link_list=[]
        for x in data_box:
            try:
                data_link=x.div.div.div.a["href"]
                link_list.append(FLIPKART_URL+data_link)
            except Exception as e:
                print(e)

# for x in link_list:
        product_html=bs(urlopen(link_list[4]).read(),'html.parser')
        product_box=product_html.find_all("div",{"class":"aMaAEs"})
        
        # NAME
        try:
            pn=(product_box[0].div.h1).text
        except Exception as e:
            print(e)
        # Rating
        product_rate=product_html.find_all("div",{"class":"_3LWZlK _1BLPMq"})
        # Heading
        product_Heading=product_html.find_all("p",{"class":"_2-N8zT"})
        # Comment
        product_comment=product_html.find_all("div",{"class":"t-ZTKy"})
        #name
        Reviewer_name=product_html.find_all("p",{"class":"_2sc7ZR _2V5EHH"})
        reviews=[]
        if len(product_rate)==len(product_Heading)==len(product_comment)==len(Reviewer_name):
            
            for x in range(len(product_rate)):
                try:
                    n=Reviewer_name[x].text
                    h=product_Heading[x].text
                    c=product_comment[x].div.div.text
                    r=product_rate[x].text

                    my_dict={'Product':pn,'Name':n,'Rating':r,'CommentHead':h,'Comment':c}        
                    reviews.append(my_dict)

                except Exception as e:
                    print(e)
# else:
#         print("need seprate loops")
    # print(reviews)
    
    client = pymongo.MongoClient("mongodb+srv://shree:Mongodb7676@cluster0.zpo2ysm.mongodb.net/?retryWrites=true&w=majority")
    db = client['review_scrap']
    review_col=db['review_scrap_data']
    review_col.insert_many(reviews)

    return render_template('result.html',reviews=reviews[0:(len(reviews)-1)])
        

if __name__=="__main__":
    # app.debug='on'
    app.run(host="0.0.0.0")
    