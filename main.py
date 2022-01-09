#importing modules
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

#reading spreadsheets of past Moon distributions
df = pd.read_csv('r18.csv')
df = dict(df.values)
df2 = dict(pd.read_csv('r17.csv').values)
df3 = dict(pd.read_csv('r16.csv').values)

prelim = []
final = []

#initializing Selenium
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=options)

#for address in the most recent CSV
for x in df:
    #get link and scrape it
    link = "https://testnet.redditspace.com/address/" + df[x] + "/token-transfers"
    driver.get(link)
    time.sleep(4)
    multiple_elements = driver.find_elements_by_class_name("pt-5")
    
    #parse all transactions
    for element in multiple_elements:
        elem = str(element.text)
        elem = elem.replace(' ', '')
        elem = elem.replace('\n', ' ')
        final_element = elem.split()
    
    #check if Moons are being transacted, and if any transactions are above 300
    for element in final_element:
        if len(element) == 85 and '0x138' in element:
            element = element.replace('0x138fAFa28a05A38f4d2658b12b0971221A7d5728', '')
            element = element.replace('→', '')
            lis.append(element)
        if 'MOON' in element and len(lis)%2 != 0:
            element = element.replace('MOON', '')
            element = element.replace(',','')
            element = float(element)
            if element > 1000:
                prelim.append(element)
                final.append(lis)
                prelim = []
            else:
                prelim = []
    
    #try to match up usernames to addresses for final results
    if len(final) != 0:
        for element in final:
            if element[0] in [value for value in df.values()]:
                element[0] = [value for value in df.keys()][[value for value in df.values()].index(element[0])]
            elif element[0] in [value for value in df2.values()]:
                element[0] = [value for value in df2.keys()][[value for value in df2.values()].index(element[0])]
            elif element[0] in [value for value in df3.values()]:
                element[0] = [value for value in df3.keys()][[value for value in df3.values()].index(element[0])]
    
    #print final suspicions
    if len(final) != 0:
        printed = 0
        for element in final:
            if element[0][0] == 'u' and element[0] != x and printed == 0:
                print(x + ': ' + str(final))
                printed = 1
    final = []
        


            
driver.quit()

