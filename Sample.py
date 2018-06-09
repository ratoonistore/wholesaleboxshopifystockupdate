import shopify

shop_url = "https://5ecbc3ae838d1b44a6c4f16037a1b6f0:4d13f266b2bc45733187cf4b7001d760@ratoon-istore.myshopify.com/admin"

shopify.ShopifyResource.set_site(shop_url)
shop = shopify.Shop.current()

product = shopify.Product.find(430577647646)
for variant in product.variants:
    variant.inventory_quantity = 100
    variant.save()
print "Done"
