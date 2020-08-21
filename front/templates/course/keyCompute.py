from hashlib import md5

if __name__ == '__main__':
    goodsname = '创业者必须课'
    istype = '1'
    notify_url = 'http://127.0.0.1:8000/course/notify_view/'
    orderid = 'YFQi7NTWY99TqMA3YFqN3H'
    orderuid = 'bhYu5iCTTABGoPS5P5kn48'
    price = '10.0'
    return_url = 'http://127.0.0.1:8000/course/6'
    token = 'f1081ec9f8ad3814f7579fc2317c4024'
    uid = '82abeee6c74dd324d735aebb'

    # bfa8ea93c00ce2f752516e92858ce464
    temp = goodsname + istype + notify_url + orderid + orderuid + price + return_url + token + uid
    print('temp:',temp)
    key = md5((goodsname + istype + notify_url + orderid + orderuid + price + return_url + token + uid).encode(
        "utf-8")).hexdigest()

    print(key)
