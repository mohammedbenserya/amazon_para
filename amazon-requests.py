import requests 
from bs4 import BeautifulSoup as bs4

import time,pandas as pd

header = {

'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en-US,en;q=0.9,fr;q=0.8',
'cache-control': 'max-age=0',
'downlink': '2.5',
'ect': '4g',
'rtt': '200',
'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
'sec-ch-ua-mobile': '?0',
'sec-ch-ua-platform': '"Windows"',
'sec-fetch-dest': 'document',
'sec-fetch-mode': 'navigate',
'sec-fetch-site': 'none',
'sec-fetch-user': '?1',
'upgrade-insecure-requests': '1',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
}


s = requests.session()
res = s.get('https://www.amazon.fr/s?rh=n%3A3162253031&fs=true&ref=lp_3162253031_sar',headers=header)

links = []
data = []
while True:
    soup= bs4(res.text,"lxml")
    prods=soup.find_all("div",{"data-component-type":"s-search-result"})

#title = ti.find_all('span',{"class":"a-size-base-plus a-color-base a-text-normal"})
    print(len(prods))
    for prod in prods:

        link = prod.find_all('a',{"class":"a-link-normal s-no-outline"})
        try:
                title = prod.find_all('span',{"class":"a-size-base-plus a-color-base a-text-normal"})
        except :
                    try:

                        title = prod.find_all('span',{"class":"a-size-medium a-color-base a-text-normal"})
                    except :
                        title = prod.find_all('span',{"class":"a-size-base a-color-base a-text-normal"})
        
        try:

                        price = prod.find_all('span',{"class":"a-offscreen"})

                        if price != []:
                            print(title[0].text.strip())
                            links.append("https://www.amazon.fr"+link[0].get("href"))
                            data.append({'brand':'','title':title[0].text.strip(),'price' : price[0].text.strip(),'CODE ASIN':prod.get("data-asin")})

                    #a-offscreen a-link-normal s-no-outline
        except :
                            pass
        if len(links) >2600:
            break
    time.sleep(1)
    #('//span[@class="a-size-base-plus a-color-base a-text-normal"]') a-price
    #//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[1]/div/div/div/div/div[3]/div[1]/h2/a/span a-last
    try:
        next=soup.select_one("li.a-last a")
        next = (next.get("href"))
        res = s.get(f'https://www.amazon.fr{next}',headers=header)
    except:
        break
print("preparing for brands..")
print(len(links))
file = open('log.txt', 'r')
lines = file.read()
file.close()
for i in range(len(links)):
        if links[i] in lines:
            continue

        res = s.get(links[i],headers=header)
        soup= bs4(res.text,"lxml")
        brand = soup.select_one("#bylineInfo")
        
        if brand != None:
            print(brand.text.strip())
            if "Marque" in brand.text.strip():
                data[i]['brand']=brand.text.strip().split(": ")[1]
            else:
                data[i]['brand']=brand.text.strip().split("boutique ")[1]
            print (data[i]['brand'])

         #driver.find_element(By.ID,'bylineInfo').text.strip()
    

        df=pd.DataFrame.from_dict([data[i]])

        df.to_csv(f"amazon.csv",mode='a',index = False,header=False)
        save = open('log.txt','a')
        save.write(f'{links[i]}\n')
        save.close()
#a-size-base a-color-base a-text-normal sp-cc-accept
