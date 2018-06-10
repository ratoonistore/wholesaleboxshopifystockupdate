#import libraries
import shopify, requests, json, math, time
from datetime import datetime
import Notify

mailSubject = "WholesaleBox Job Run Started at Server : " + datetime.now().strftime('%d-%m-%Y %H:%M:%S')
mailBody = "WholesaleBox Job Run Started at Server: " + datetime.now().strftime('%d-%m-%Y %H:%M:%S')

Notify.sendMail(mailSubject, mailBody)
    
#ratoon shop authentication url
shop_url = "https://5ecbc3ae838d1b44a6c4f16037a1b6f0:4d13f266b2bc45733187cf4b7001d760@ratoon-istore.myshopify.com/admin"

#getting product count
urlToGetProductCount = "https://5ecbc3ae838d1b44a6c4f16037a1b6f0:4d13f266b2bc45733187cf4b7001d760@ratoon-istore.myshopify.com/admin/products/count.json?vendor=Wholesalebox"
urlToGetProductCount_Response = requests.get(urlToGetProductCount)
productCount_Json = json.loads(urlToGetProductCount_Response.content)
totalProductCount = int(productCount_Json['count'])

#setting product limit
productLimit = 50

#total pages available
totalpage = int(math.ceil(totalProductCount/productLimit)) + 1;

#Setting our shop
shopify.ShopifyResource.set_site(shop_url)
shop = shopify.Shop.current()

#setting product run count
product_SKU = "1234"
productRunCount = 0;
instockProductRunCount = 0;
outstockProductRunCount = 0;

Failed_Products_SKU = ""
Failed_Products_SKU_Count = 0

for i in range(1, totalpage):
    products = shopify.Product.find(vendor = "Wholesalebox", limit = productLimit, page = i)
                
    for product in products:
        productRunCount = productRunCount + 1
        
        for variant in product.variants:
            
            try:

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

            except:
                Failed_Products_SKU = Failed_Products_SKU + ", " + product_SKU
                Failed_Products_SKU_Count = Failed_Products_SKU_Count + 1
                continue

InstockRunCountReport = "InStock Products updated in shopify: " + str(instockProductRunCount)
OutstockRunCountReport = "OutStock Products updated in shopify: " + str(outstockProductRunCount)
FailedProductsReport = "List of failed products: " + Failed_Products_SKU
FailedProductsCount = "Cout of failed products: " + str(Failed_Products_SKU_Count)

mailSubject = "WholesaleBox Job Run Report in Server for : " + datetime.now().strftime('%d-%m-%Y %H:%M:%S')
mailBody = """<html>
      <head></head>
      <body>
        <h3>""" + mailSubject + """</h3>
        <br>
        <hr>
        <br>
        <ul>
        <li><h4>""" + InstockRunCountReport + """</h4></li>
        <br>
        <li><h4>""" + OutstockRunCountReport + """</h4></li>
        <br>
        <li><h4>""" + FailedProductsCount + """</h4></li>
        <br>
        <li><h4>""" + FailedProductsReport + """</h4></li>
        </ul>
      </body>
    </html>"""

Notify.sendMail(mailSubject, mailBody)
