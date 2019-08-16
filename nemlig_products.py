
# coding: utf-8

# In[34]:

import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)
from IPython.display import display

import requests
from bs4 import BeautifulSoup as bs


# In[35]:

#driver.quit()
## Selenium ##
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re


driver = webdriver.Chrome('D:\_gDrive\_sync_folder\selenium\chromedriver.exe')

#driver = selenium.webdriver.Chrome() 
#f = webdriver.Chrome("chromedriver.exe")
#f = webdriver.Firefox()

#driver=f

#open page


driver.get("https://www.nemlig.com/varer")
time.sleep(3)

cookie_sel=driver.get_cookie
url="https://www.nemlig.com/varer"

page_sel = driver.page_source

#driver.quit()
#page
#cookie_sel



url="https://www.nemlig.com/varer"

page = requests.get(url)

soup = bs(page.content, 'html.parser')
soupL = bs(page.content, 'lxml')


# Cleaners
def remove_all_whitespace(x):
    """
    Returns a string with any blank spaces removed.
    """
    try:
        x = x.replace("		", "")        
        x = x.replace("  ", "")

    except:
        pass
    return x


def trim_the_ends(x):
    """
    Returns a string with space on the left and right removed.
    """
    try:
        x = x.strip(' \t\n\r')
    except:
        pass
    return x


def remove_unneeded_chars(x):
    """
    Returns the string without the unneeded chars
    """
    try:
        x = x.replace("$", "").replace("RRP", "")
        x = x.replace("\r", "").replace("\n", "").replace("\t", "")
    except:
        pass
    return x


grp=[]
href=[]
desc=[]
for url in soup.find_all('a'):
                 hrf=url.get('href')
                 href.append(hrf)

                 txt=url.get_text()
                 txt=txt.replace('\r','')   #klar tekst element
                 tx2=trim_the_ends(str(txt))
                 tx3=tx2.lstrip(' ')
                 dsc=tx3
                 desc.append(dsc)
                    
                 gp=''
                 gp=str(hrf).split('/')
                 grp.append(gp[1:])  # removes first element of list (',')
                    
links=pd.DataFrame(href)

links.columns=['href']
links['desc']=desc
links['grp']=grp
links['web_link']=""+'https://www.nemlig.com' + links.href


# In[38]:

links


# In[39]:
# cleanup links
keep_rc=[]
for element in grp:
    gp=element
    #print(gp,len(gp))
    #print(gp[0])
    if len(gp)>0 and gp[0]=='varer': 
        keep_rec=1
    else: keep_rec=0    
    
    keep_rc.append(keep_rec)
    #products.append(gp)
    
links['keep_rec']=keep_rc

links_x=links.loc[links.keep_rec==1] 

links_x.reset_index
links_x


url_v=links_x['web_link'].values

#url_v[60:70]


# In[42]:

links_x.sort_values(['href'],ascending=[True])
links_x.reset_index
links_x

print(links_x)

######################
# get links to api   #
######################
def get_page_overview(json_content):
    http_str=[]
    #js_prodX=[]

    cnt_=0
    for jc in json_content:
        cnt_ +=1
        head=""
        try:
            head_=jc['Heading']
        except:
            ''
 
        try:
            prod_grp_=jc['ProductGroupId']
            http_str_="https://www.nemlig.com/webapi/" + json_combi + "/" + json_time + "/1/0/Products/GetByProductGroupId?productGroupId=" + prod_grp_ 
    #        products_=s.get(http_str_)
            http_str.append(http_str_)
        except:
            ''
    return http_str


import json
import requests
import pandas as pd
import re
from bs4 import BeautifulSoup as bs

s = requests.Session()



ccnt_=0
prodXXX=[]
deep_links=[]
for ur in url_v[3:4]:
    ccnt_+=1
    deep_link_=[]
    if ccnt_ >=0:
        print(ur)
        
        s.get(ur)
        time.sleep(2)

        #page = requests.get(ur)
        page = s.get(ur)
        cookie=s.cookies

        soupH = bs(page.content, 'html.parser')

        scripts=soupH.find_all('script')
        print(scripts)

        deep_link_=soup.find_all("a[href*=/varer/]")
        deep_links.append(deep_link_)

        p=re.compile('contentAsJson')

        cn=0
        cont_js=""
        for sc in scripts:
            cn+=1
            #print(cn,sc)
            if p.search(str(sc)):
                cont_js=sc
                #print(cont_js)

        #type(cont_js)
        cont_js=cont_js.string

        conj_js = cont_js.replace('\n', '').replace('\r', '').replace('\t','').replace(';','')
        json_string=conj_js[19:]

        ds = json.loads(json_string)

        json_id = ds['MetaData']['Id']

        json_combi=ds['Settings']['CombinedProductsAndSitecoreTimestamp']
        json_time=ds['Settings']['TimeslotUtc']

        json_cont_=ds['content']
        
        #print(json_cont_)
        http_strX=get_page_overview(json_cont_)
        
        
        
        
        #init page -  maybe token issue
        driver.get(http_strX[0])
        driver.page_source
        time.sleep(2)
        
        
        #s.get(http_strX[0]).json()
        prodX_=[ur]      # page group link
        for ht in http_strX:
            prodx0_=''
            try:
                prodx0_=s.get(ht).json()
                prodX_.append(prodx0_)
            except:
                ''
            print(len(prodX_))
        #print(prodX_)
        try:
            prodXXX.append(prodX_)
            prodXXX_url.append(ur)
        except:
            ''

# In[64]:
#export to json
filename_json='nemlig_prod_2017.json'
with open(filename_json,'w') as f:
    json.dump(prodXXX, f)
f.close      
#data_prodXXX=prodXXX



#######################
# export to flat file #
#######################
# import from json
filename_json='nemlig_prod_2017.txt'
with open(filename_json,'r') as f:
    data_prodXXX=json.load(f)

import pandas as pd
import json

def create_file(fname):
    f = open(fname, 'w', encoding="utf-8")
    print("file '" + str(fname) + "'  created")
    
def append2file(fname, txt_string):
    f = open(fname, 'a', encoding="utf-8")
    f.write(txt_string)
    f.write("\n")
    f.close()
    print("lines appended to '" + str(fname)+ "'")


prodXXX=data_prodXXX

#create flat file
fn_="nemlig_products_20170531.csv"
keys=['Category', 'Description', 'Id', 'Name', 'Price', 'PrimaryImage',
      'SearchDescription', 'UnitPrice', 'Url']
fn_="nemlig_export_prod.csv"
head_=str(keys)[1:-1]

create_file(fn_)
append2file(fn_, head_)

error_log=[]
cnt_=0
for p1 in data_prodXXX:
    cnt_+=1
    if cnt_>=0:
        try:
            url_page=p1[0]
            p2=p1[1:]
            
            for p3 in p2:
                prod_line=p3['Products']
                for prod_uniq in prod_line:
                    mydict=prod_uniq
                    out_prod=str([mydict.get(key) for key in keys if key in mydict])[1:-1]
                    print(out_prod)
                    append2file(fn_, out_prod)

        except:
            error_log.append("p1:" + str(p1 ) 
            + "\n" + str(p2) + "\n" + str(p3) 
            + "\n" + str(mydict) + "\n" + str(prod_uniq) 
            + "\n" + str(out_prod) + "")


