import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import urllib.request as urllib2
from termcolor import colored

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
    req = requests.get("https://api.unsplash.com/search/photos?page=1&query="+word+"&client_id=WnqByO4bcBwmoasQWIT_aXxLNDlAq-QQXXBcWDRcg0I")
    data = req.json()
    filename = str(word) + ".jpg"
    for res in data['results']:
        if res['height'] > res['width']:
            img.append(res)
        else: continue
    if img != []:
        last_res = max(img,key=lambda item:item['likes'])
        urllib2.urlretrieve(last_res['urls']['small'], "./images/"+filename)
        print (word + " Downloaded! ✔")
    else:
        row += 1
        undefined_word.update_cell(row,1,f"{word}")
        undefined_word.update_cell(row,2,"Undefined")
        print (colored(word + " Undefined! X",'red'))

print (colored('------------------\nSucessfully Download all your images!:)', 'green'))
