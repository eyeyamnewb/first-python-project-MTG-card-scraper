#author eyeyamnewb
import selenium
import time
import csv
from selenium import webdriver
from bs4 import BeautifulSoup

#enable the launch of chrome remotely
browser = webdriver.Chrome()

#create a csv file for the data to be written into following the title given 
file = open("cards data.csv","w")
writer = csv.writer(file)
writer.writerow(["title","color","set","type","card set number","rarity","foil","price"])

#for this gray code refer to line 175+ in green
#writer.writerow(["title","color","set","type","card set number","rarity","foil"," us price", " my price"])

#variable for web source to be scrape from 
search_queary = "https://starcitygames.com/search/?search_query="
site_link = "https://starcitygames.com"

#variable for where the card source will be called upon
txt_file_1 = "for test run.txt"

#variable for links that has been extract from site and will be use as an extention for site_link
txt_file_2 = "site link.txt"

#basic variable, list & dictionary set up for colour identity
colorless ="colorless"
white ="white"
blue ="blue"
black ="black"
red ="red"
green ="green"

ColorDict = {
    'color-w': white,
    "color-b":black,
    "color-u":blue,
    "color-r":red,
    "color-g":green,
    }

GuildTheme = {
    white:[white],
    black:[black],
    blue:[blue],
    red:[red],
    green:[green],
    'azorious' : [white,blue],
    "boros" : [white,red],
    "dimir" : [black,blue],
    "golgari" : [black,green],
    "gruul" : [red,green],
    "izzet" : [blue,red],
    "orzhov" : [white,black],
    "rakdos" : [black,red],
    "selesnya" : [white,green],
    "simic" : [blue,green],
    "abzhan" : [white,black,green],
    "bant" : [white,blue,green],
    "esper" : [white,black,blue],
    "grixis" : [black,blue,red],
    "jeskai" : [white,blue,red],
    "jund" : [black,green,red],
    "mardu" : [white,black,red],
    "naya" : [white,green,red],
    "sultai" : [black,blue,green],
    "temur" : [blue,green,red],
    "glint" : [black,blue,green,red],
    "dune" : [white,black,green,red],
    "ink" : [white,blue,green,red],
    "witch" : [white,black,blue,green],
    "yore" : [white,black,blue,red], 
    "rainbow" : [white,black,blue,red,green],
    "colorless":[]}

"########################### function start here  #############################"             

def txt_reader(target_file):   #open data files to be and extract read by python
    file = open(target_file,"r")
    data = file.read()
    data = data.split("\n")
    file.close
    return data

def Overwriter(target_file): #overwrite existing file with blanks
    file = open(target_file, 'w')
    file.write("")        
    
def link_scraped(scrape_result): #export link scraped into file 2
    file = open("site link.txt", "a")
    for links in {scrape_result}:
        file.write(links)        
    file.write("\n")
    file.close()
    
def link_scraper(): #scrape product link after searching for the cards in the search bar
       
    for x in txt_reader(txt_file_1): # error here???
        searched = search_queary + str(x)        
        browser.get(searched)
        time.sleep(5)
        
        result = browser.page_source
        result = BeautifulSoup(result,"html.parser")
        
        for egg in result.findAll("a",attrs={"class":"item-title-link"}):
            
            egg = str(egg.get("href"))
            egg = egg 
            
            link_scraped(egg)

def card_targeted(target): #scrape link will direct to target card

    data_extract = site_link + str(target)    

    if data_extract == site_link: #this is just for trouble shooting
        data_extract = site_link + "/chalice-of-the-void-sgl-mtg-mrd-150-enn/"
        result = browser.page_source
        result = BeautifulSoup(result,"html.parser")
        return result
    else:
        browser.get(data_extract)
        time.sleep(5)
            
        result = browser.page_source
        result = BeautifulSoup(result,"html.parser")
        return result

def TRUE_identity(results1): #prevent duplication and the card color identity

    mana_no_dupe =  list(dict.fromkeys(results1))
    
    for x in GuildTheme:
        if mana_no_dupe == GuildTheme[x] :
            return x
        
    
Overwriter(txt_file_2) #clear out link file
"###################### func end , process start  #############################"
link_scraper() #starts the process of scraping the card list 

for target in txt_reader(txt_file_2):
    identity_result = [] 
    #fetch up web attribute base on class and id
    card = card_targeted(target)
    card_color = card.findAll("svg",attrs={"class":"svg-inline--fa"})
    card_title    = card.find("h1",attrs={"class":"productView-title"})
    card_set      = card.find("dd",attrs = {"id":"custom-field--Set"})
    card_type     = card.find("dd",attrs = {"id":"custom-field--Card Type"})
    card_num      = card.find("dd",attrs ={"id":"custom-field--Collector Number"})
    card_rarity   = card.find("dd",attrs = {"id":"custom-field--Rarity"})
    card_finished = card.find("dd",attrs = {"id":"custom-field--Finish"})
    card_price    = card.find("span", attrs= {"class": "price price--withoutTax"}) 
    
    for color in ColorDict :
        for mana in card_color:
            mana = mana.get("class")
            
            mana = [color_list for color_list in mana if color in color_list] #list if attribute fit ColorDict criteria

            for true_mana in mana:
               
                mana = ColorDict[str(true_mana)]
                
                identity_result.append(mana)
    identity = str(TRUE_identity(identity_result))
        
    for title,set,type,num_code,rarity,foil,price in zip(card_title,card_set,card_type,card_num,card_rarity,card_finished,card_price):
        price = float(price.text.replace('$',''))
                
        """USPrice = (price * 1.35) 
        MyPrice = (price * 1.15)    this whole section is for my rate and local usd rate rounded 
        
        if round(price) >= price:
        round_USPrice = round(USPrice) 
        round_MyPrice = round(MyPrice)          
        if round_USPrice and round_MyPrice < USPrice and MyPrice :
            USPrice = round_USPrice + 1
            MyPrice = round_MyPrice + 1
           
        else:
            USPrice = round_USPrice
            MyPrice = round_MyPrice"""
           
        my_card = [title,identity,set,type,num_code,rarity,foil,price]
        #my_card = [title,identity,set,type,num_code,rarity,foil,USPrice,MyPrice] for section above
        writer.writerow(my_card)  
        print(my_card)    
       
browser.quit()     
file.close()  
    