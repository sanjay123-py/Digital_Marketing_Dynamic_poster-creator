import sys
from PIL import ImageDraw,ImageFont,Image
from bs4 import BeautifulSoup
from urllib import request
import requests
import re
import logging
import qrcode
# logging.basicConfig(filename='first.log',filemode='w',level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
class Scraper:
    def __init__(self,url):
        self.url=str(url)
        self.result = request.urlopen(self.url)
        self.doc = BeautifulSoup(self.result, 'html.parser')
        try:
            self.font1 = ImageFont.truetype('/Users/sanjay/Desktop/yoscrap/Montserrat-BlackItalic.ttf',size=30)
            self.font2 = ImageFont.truetype("/Users/sanjay/Desktop/yoscrap/Montserrat-SemiBold.ttf", size=25)
            self.font3 = ImageFont.truetype("/Users/sanjay/Desktop/yoscrap/Montserrat-medium.ttf", size=23)
        except Exception as e:
            print(e)
    def get_img(self):
        try:
            img = self.doc.find(["img"], id='product-image')
            img_data = requests.get(img['src']).content
            with open("image.jpg", 'wb+') as f:
                f.write(img_data)
            # logging.info("Image Scrapped Successfully")
            img=self.doc.find(['img'],class_='img-responsive')
            img_data=requests.get(img['src']).content
            with open('title.jpg','wb+') as f:
                f.write(img_data)
        except Exception as e:
            print("exception Happened:",e)
            # logging.error("Error happened: ",e)
    def title_string_mani(self,x):
        if (len(x) > 30):
            for i in range(30, len(x)):
                if (x[i] == " "):
                    title1 = x[:i] + '\n' + x[i:]
                    break;
        return title1
    def get_data(self):
        try:
            self.title=self.doc.find_all(['h1'],class_="single-product-title")[0].string
            self.title1=self.title_string_mani(self.title)
            self.offer=self.doc.find(['b'],text=re.compile('U.*')).text[17:]
            self.price=self.doc.find_all(['span'], id='sale-price')[0].text
            self.duration=self.doc.find(['span'], text=re.compile("Month.*")).string[:7]
            self.mode=self.doc.find(['span'],text=re.compile("Online")).string
            # logging.info("Data Collected Successfully")
        except Exception as e:
            print(e)
            # logging.error("Error happened: ",e)
    def get_qrcode(self):
        try:
            self.img=qrcode.make(str(self.url))
            self.img.save("qr.jpg")
            # logging.info("QRCODE sucessfullu created")
        except Exception as e:
            print(e)
            # logging.error("Error: ",e)
    def image_accumulate(self):
        try:
            self.template = Image.open('/Users/sanjay/Desktop/yoscrap/template.png').resize((739, 1135))
            self.pic = Image.open('/Users/sanjay/Desktop/yoscrap/Border.png')
            self.pic.paste(self.template, (32, 36, 771, 1171))
            self.title_template=Image.open('/Users/sanjay/Desktop/yoscrap/title.jpg').resize((482,104))
            self.pic.paste(self.title_template, (154, 70, 636, 174))
            self.main_template = Image.open('/Users/sanjay/Desktop/yoscrap/image.jpg').resize((523, 451))
            self.pic.paste(self.main_template, (139, 259, 662, 710))
            self.draw = ImageDraw.Draw(self.pic)
            self.draw.text((120, 721),self.title1, font=self.font1,fill='rgb(0,0,0)')
            self.draw.text((60,826),"Course Fee: ",fill='rgb(0,0,0)',font=self.font2)
            self.draw.text((60,900),'Duration: ',fill='rgb(0,0,0)',font=self.font2)
            self.draw.text((60,974),'Use Coupon: ',fill='rgb(0,0,0)',font=self.font2)
            self.draw.text((60,1048),'Training Mode: ',fill='rgb(0,0,0)',font=self.font2)
            #for fee data
            self.draw.text((220,826),self.price,fill='rgb(255,0,0)',font=self.font3)
            #for duration data
            self.draw.text((192,900),self.duration,fill='rgb(0,0,0)',font=self.font3)
            #for coupon data
            self.draw.text((232,974),self.offer,fill='rgb(0,0,0)',font=self.font3)
            #for training mode
            self.draw.text((260,1048),self.mode,fill='rgb(0,0,0)',font=self.font3)
            # logging.info("Data Pasted successfully into the poster")
            self.qr=Image.open('qr.jpg').resize((221,221))
            self.pic.paste(self.qr,(521,883,742,1104))
            self.pic=self.pic.save('/Users/sanjay/Desktop/yoscrap/'+'Poster'+self.title[:10]+'.png')
            # logging.info("Banner created Successfully../../../../")
        except Exception as e:
            print(e)
            # logging.error("Error Happened: ",e)
    # def get(self):
    #     self.mode = self.doc.find(['span'], text=re.compile("Online")).string
    #     print(self.mode)
# scrap=Scraper('https://yoshops.com/products/blockchain-developer-internship-training-program1')
# scrap.get_img()
# scrap.get_data()
# scrap.get_qrcode()
# scrap.image_accumulate()




######## !!!!!!!!!!! ''''AFTER GIVING THE LINK PRESS 0 TO SAVE THE POSTER'''' !!!!!!!!!! ############



while(True):
    print('Enter 1 for creating banner:')
    print('Enter 0 for exit and to SAVE the poster:')
    n=int(input())
    if(n==1):
        print('Enter the yoshops course link:')
        str1=str(input())
        scrap=Scraper(str1)
        scrap.get_img()
        scrap.get_data()
        scrap.get_qrcode()
        scrap.image_accumulate()
    else:
        break
sys.exit(0)

