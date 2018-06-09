#import libraries
import shopify, requests, json, math, time, os, smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from datetime import datetime

#ratoon shop authentication url
shop_url = "https://5ecbc3ae838d1b44a6c4f16037a1b6f0:4d13f266b2bc45733187cf4b7001d760@ratoon-istore.myshopify.com/admin"

#getting product count
urlToGetProductCount = "https://5ecbc3ae838d1b44a6c4f16037a1b6f0:4d13f266b2bc45733187cf4b7001d760@ratoon-istore.myshopify.com/admin/products/count.json?vendor=Wholesalebox"
urlToGetProductCount_Response = requests.get(urlToGetProductCount)
productCount_Json = json.loads(urlToGetProductCount_Response.content)
totalProductCount = int(productCount_Json['count'])

#setting product limit
productLimit = 1

#total pages available
totalpage = int(math.ceil(totalProductCount/productLimit)) + 1;

#Setting our shop
shopify.ShopifyResource.set_site(shop_url)
shop = shopify.Shop.current()

#setting product run count
productRunCount = 0;
instockProductRunCount = 0;
outstockProductRunCount = 0;

for i in range(1, 2):
    products = shopify.Product.find(vendor = "Wholesalebox", limit = productLimit, page = 37)
    
    for product in products:
        productRunCount = productRunCount + 1
        print("\n\tPages in progress : " + str(i) + " of " + str(totalpage))
        print("\tProducts in progress : " + str(productRunCount) + " of " + str(totalProductCount))
        
        for variant in product.variants:
            product_SKU = variant.sku
            wholesalebox_Api_Url = 'http://www.wholesalebox.in/index.php?route=feed/feed/checkStock&token=a5a954e23x57d100&model=' + product_SKU
            response = requests.get(wholesalebox_Api_Url)
            wholesaleboxQty = 0
            shopifyQty = variant.inventory_quantity
            
            if(response.ok):    
                data = json.loads(response.content)
                wholesaleboxQty = int(data['quantity'])
                
            if(shopifyQty >= 1 and wholesaleboxQty <= 3):       #in-stock => out-stock
                variant.inventory_quantity = 0
                variant.save()
                instockProductRunCount = instockProductRunCount + 1
                
            elif(shopifyQty <= 0 and wholesaleboxQty > 3):     #out-stock => in-stock
                variant.inventory_quantity = wholesaleboxQty
                variant.save()
                outstockProductRunCount = outstockProductRunCount + 1
                
        os.system('cls')

print "\n \t =======COMPLETED========="
print "\n \t InStock Products updated in shopify:",instockProductRunCount
print "\n \t OutStock Products updated in shopify:",outstockProductRunCount

InstockRunCountReport = "InStock Products updated in shopify:" + str(instockProductRunCount)
OutstockRunCountReport = "OutStock Products updated in shopify:" + str(outstockProductRunCount)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("ratoonistore@gmail.com", "RatooniStore@2017")

fromaddr = "jobrun@ratoonistore.com"
toaddr = "ratoonistore@gmail.com"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "WholesaleBox Job Run Report for : " + datetime.now().strftime('%d-%m-%Y %H:%M:%S')
 
body = """<html>
  <head></head>
  <body>
    <p><br><b>WholesaleBox Job Run Report for : """ + datetime.now().strftime('%d-%m-%Y %H:%M:%S') + """</b><br><hr><br>""" + InstockRunCountReport + """
       <br><br> """ + OutstockRunCountReport + """<br><br>
    </p>
  </body>
</html>"""
msg.attach(MIMEText(body, 'html'))

text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
