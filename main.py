import requests
from bs4 import BeautifulSoup as bs
import streamlit as st

st.set_page_config(page_title='Flipkart Review Scraper', page_icon=":mag:", layout='wide', initial_sidebar_state='auto')
st.title('Flipkart Review Scraper')
inp= st.text_input("Enter Search Term", "Redmi Phones")
url="https://www.flipkart.com/search?q=" + inp
headers={'Accept-Encoding': 'identity, deflate, compress, gzip','Accept': '*/*', 'User-Agent': 'python-requests/1.2.0'}
st.write('Fetching search results...')
st.write(str(url))
a=requests.get(url,headers=headers,)
st.write(str(a)+str(a.headers)+str(a.cookies))
st.write(str(a.request.headers))
dat=bs(a.text,'html.parser').findAll("div",{"class":"_1AtVbE col-12-12"})[2:][:-2]
st.write("dat: "+str(dat))
products=[]
for i in range(len(dat)):
    try: products.append("https://www.flipkart.com"+dat[i].div.div.div.a["href"])
    except: continue
def get_review(link):
    st.write(f'Fetching reviews for {link}...')
    prod=requests.get(link,headers=headers)
    prod=bs(prod.text,"html.parser")
    t=prod.find("span",{"class":"B_NuCI"})
    try: name=t.text
    except: name=inp
    rev=prod.findAll("div",{"class":"col _2wzgFH"})
    return name,[[i.div.div.text,i.div.p.text,i.find("div",{"class":""}).div.text,i.find("p",{"class":"_2sc7ZR _2V5EHH"}).text,i.findAll("p",{"class":"_2sc7ZR"})[1].text] for i in rev]

if st.button('Get Reviews'):
    st.write("Tapped Button")
    with st.spinner('Fetching reviews...'):
        st.write("Starting Spinning")
        st.write(str(products))
        for i in products:
            st.write("Product Selected")
            r=get_review(i)
            if r[0]==inp: continue
            st.subheader(f'Product: {r[0]}')
            for j in r[1]:
                st.markdown(f"""
                    **Rating:** {'⭐'*int(j[0])}  
                    **Title:** {j[1]}  
                    **Review:** {j[2]}  
                    **Reviewer:** {j[3]}  
                    **Date:** {j[4]}  
                """)
            st.write('='*88)