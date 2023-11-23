from flask import Flask, render_template, request
from bs4 import BeautifulSoup as bs
import requests
import streamlit as st

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    reviews = []
    if request.method == 'POST':
        inp = request.form.get('product')
        url = "https://www.flipkart.com/search?q=" + inp
        dat = bs(requests.get(url).text, 'html.parser').findAll("div", {"class": "_1AtVbE col-12-12"})[2:][:-2]
        products = []
        for i in range(len(dat)):
            try:
                products.append("https://www.flipkart.com" + dat[i].div.div.div.a["href"])
            except:
                continue

        for i in products:
            r = get_review(i)
            if r is not None: reviews.append(r)

    return render_template('index.html', reviews=reviews)

def get_review(link):
    prod = requests.get(link)
    prod = bs(prod.text, "html.parser")
    t = prod.find("span", {"class": "B_NuCI"})
    if t is None: return None
    name = t.text
    rev = prod.findAll("div", {"class": "col _2wzgFH"})
    return name, [[i.div.div.text, i.div.p.text, i.find("div", {"class": ""}).div.text, i.find("p", {"class": "_2sc7ZR _2V5EHH"}).text, i.findAll("p", {"class": "_2sc7ZR"})[1].text] for i in rev]

if __name__ == '__main__':
    app.run(debug=True)