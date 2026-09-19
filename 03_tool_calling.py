#这是个假的产品数据库
products = {
    "A产品": 1999,
    "B产品": 3999,
    "C产品": 899
}

def get_price(product_name):
    if product_name in products:
        return products[product_name]
    else:
        return -1

    #测试函数能不能用
print(get_price("A产品"))
print(get_price("D产品"))