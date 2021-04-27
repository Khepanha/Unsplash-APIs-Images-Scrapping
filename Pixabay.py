import gspread
from oauth2client.service_account import ServiceAccountCredentials
from termcolor import colored
import requests
import urllib.request as urllib2
import shutil

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

sheet = client.open("Scrap Unsplash API python").sheet1
undefined_word = client.open("Scrap Unsplash API python").worksheet('Undefined Word')

words = sheet.col_values(2)
words.pop(0)
row = 1
for word in words:
    img = []
    req = requests.get("https://pixabay.com/api/?key=21280539-53361c7eaa084b788ec5c194e&q="+word+"&image_type=photo")
    data = req.json()

    filename = str(word) + ".jpg"
    for res in data['hits']:
        # if res['imageHeight'] > res['imageWidth'] and word.lower() in res['tags'] or word.lower()+"s" in res['tags']:
        if res['imageHeight'] > res['imageWidth']:
            img.append(res)
        else: continue
    if img != []:
        last_res = max(img,key=lambda item:item['likes'])
        img_req = urllib2.build_opener()
        img_req.addheaders = [{'User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64)'}]
        urllib2.install_opener(img_req)
        urllib2.urlretrieve(last_res['largeImageURL'], "./images/"+filename)
        print (word + " Downloaded! ✔")
    else:
        row += 1
        undefined_word.update_cell(row,1,f"{word}")
        undefined_word.update_cell(row,2,"Undefined")
        print (colored(word + " Undefined! X", 'red'))

print (colored('------------------\nSucessfully Download all your images!:)','green'))
