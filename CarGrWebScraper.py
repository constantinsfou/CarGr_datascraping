import requests
from bs4 import BeautifulSoup
import lxml
import re
import datetime
import pandas as pd

def CarGrDataParser_New(urllink):
    html_text = requests.get(urllink)
    soup = BeautifulSoup(html_text.content, "html.parser")
    
    # regular expression to pick up kilometers
    re1 = re.compile("(\d{1,3}\.\d{3}|\d{1,3})")
    # regular expression to pick up date
    re2 = re.compile("\d{2}/\d{4}")
    
    Brand = []; Price = []; Date = []; EngVol = []; EngPow = []; Fuel = []; Mileage = []; Gear = []
    
    # find all the tags that contain car data
    results = soup.find_all("div", class_="row p-2 position-relative no-gutters")
    
    for result in results:
        
        Brand.append(result.find("div", class_="title font-size-xl title").text.split()[0]) # brand)
        
        price = result.find("span", class_="price-no-decimals").text # price
        price = int(price.replace('.',''))
        Price.append(price)
                     
        date = result.find("span", class_="key-feature", title="Χρονολογία")    # date
        if date:
            date_num = datetime.datetime.strptime(re2.findall(date.text)[0], '%m/%Y')
        else:
            date_num = 'n/a'
        Date.append(date_num)
        
        enginecc = result.find("span", class_="key-feature", title="Κυβικά")
        if enginecc:
            enginecc = enginecc.text
            enginecc = re.findall(r'\b\d+\b',enginecc)
            engVol = int(enginecc[0])*1000 + int(enginecc[1])
            engPow = int(enginecc[2])
        else:
            engVol = 'n/a'
            engPow = 'n/a'
        EngVol.append(engVol)
        EngPow.append(engPow)
        
        fuel = result.find("span", class_="key-feature", title="Καύσιμο")
        if fuel:
            fuel = re.findall('\w+',fuel.text)
        else:
            fuel = 'n/a'
        Fuel.append(fuel)
                     
        km = result.find("span", class_="key-feature", title="Χιλιόμετρα")
        if km:
            km = re1.search(km.text).group(1)
            km_num = int(km.replace('.',''))
        else:
            km_num = 'n/a'
        Mileage.append(km_num)
                     
        gear = result.find("span", class_="key-feature", title="Σασμάν")
        if gear:
            gear = True
        else:
            gear = False
        Gear.append(gear)
                     
    return {"brand":Brand,
            "price":Price,
            "kilometers":Mileage,
            "engine_cc":EngVol,
            "engine_bhp":EngPow,
            "date":Date,
            "fuel":Fuel,
           "gear":Gear}
  
  CarData = {"brand":[],
          "price":[],
          "kilometers":[],
          "engine_cc":[],
          "engine_bhp":[],
          "date":[],
          "fuel":[],
          "gear":[]}

  # loop through pages of available ads. I got 21 'cause there's currently 22 pages available. May be different. In a later version, I will just 'click' the 'Next Page' button.
for ppp in range(0,21):
    PageNum = ppp + 1;
    urllink = "https://www.car.gr/classifieds/cars/?category=11&condition=used&doors=4-5&engine_size-from=%3E1000&fromfeed=1&fuel_type=1&fuel_type=8&mileage-to=%3C200000&pg="+ "%d"%PageNum +"&price-from=%3E8000&price-to=%3C25000&registration-from=%3E2015&rg=2"
    #html_text = requests.get(urllink)
    
    CarDataTemp = CarGrDataParser_New(urllink)
    
    CarData['brand'].extend(CarDataTemp['brand'])
    CarData['price'].extend(CarDataTemp['price'])
    CarData['kilometers'].extend(CarDataTemp['kilometers'])
    CarData['engine_cc'].extend(CarDataTemp['engine_cc'])
    CarData['engine_bhp'].extend(CarDataTemp['engine_bhp'])
    CarData['date'].extend(CarDataTemp['date'])
    CarData['fuel'].extend(CarDataTemp['fuel'])
    CarData['gear'].extend(CarDataTemp['gear'])
            
      
df = pd.DataFrame(CarData)
df.to_csv(path_or_buf="CarGr_data.csv", encoding='utf-8-sig') # this encoding preserves some texts in Greek

    
