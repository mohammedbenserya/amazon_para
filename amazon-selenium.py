
from selenium import webdriver
from selenium.webdriver.common.by import By

import time,pandas as pd
driver = webdriver.Chrome()


driver.get("https://www.amazon.fr/s?rh=n%3A3162253031&fs=true&ref=lp_3162253031_sar")


data=[]
links=[]
try:
    driver.find_element_by_id('sp-cc-accept').click()
except :
    pass
i=0
#a-last
while True:

    time.sleep(1)
    prod = driver.find_elements(By.XPATH,"//div[@data-component-type='s-search-result']")
    
    for p in range(len(prod)):
        code=(prod[p].get_attribute("data-asin"))
        try:
            title = (prod[0].find_elements_by_xpath('//span[@class="a-size-base-plus a-color-base a-text-normal"]')[p].text)
        except :
            try:
                title = (prod[0].find_elements_by_xpath('//span[@class="a-size-medium a-color-base a-text-normal"]')[p].text)
            except :
                title = (prod[0].find_elements_by_xpath('//span[@class="a-size-base a-color-base a-text-normal"]')[p].text)
        
            try:
                price=""
                price = prod[0].find_elements_by_xpath('//span[@class="a-price"]')[p].text.strip()
                if price == "":
                    continue
                data.append({'brand':'','title':title,'price' : price,'CODE ASIN':code})
            #a-offscreen
            except :
                    continue
        links.append(prod[0].find_elements_by_xpath('//a[@class="a-link-normal s-no-outline"]')[p].get_attribute('href'))
        i+=1
        if i > 2600:
            break
        
        """Subdriver = webdriver.Chrome()
        Subdriver.get(link)
        brand = Subdriver.find_element_by_id('bylineInfo')
        print (brand.text)
        Subdriver.close()"""
    try:
        next = driver.find_element(By.XPATH,"//li[@class='a-last']/a").get_attribute('href')
        driver.get(next)
    except :
        print("none")
        break
    
print("preparing for brands..")
print(len(links))
file = open('log.txt', 'r')
lines = file.read()
file.close()
for i in range(len(links)):
    if links[i] in lines:
        continue
    driver.get(links[i])
    try:
        brand = driver.find_element(By.ID,'bylineInfo').text.strip()
        if "Marque" in brand:
            data[i]['brand']=brand.split("Marque : ")[1]
        else:
            data[i]['brand']=brand.split("boutique ")[1]
    except:
        data[i]['brand']="Unknown"
        
    


    df=pd.DataFrame.from_dict([data[i]])

    df.to_csv(f"amazon.csv",mode='a',index = False,header=False)
    save = open('log.txt','a')
    save.write(f'{links[i]}\n')
    save.close()
#a-size-base a-color-base a-text-normal sp-cc-accept
driver.close()

