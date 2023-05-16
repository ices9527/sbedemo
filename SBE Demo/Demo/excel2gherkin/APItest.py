from urllib import request

url = 'http://service-price.sit.online.lenovo.com/api/v1/price/getPrice?productCodes=F0DY002AUS&contextString=US%7CB2C%7Cusweb%7CEN'
# mockUrl = 'http://rap2api.taobao.org/app/mock/222718/addToCart'
with request.urlopen(url) as f:
    data = f.read()
    print('Status:', f.status, f.reason)
    for k, v in f.getheaders():
        print('%s: %s' % (k, v))
    print('Data:', data.decode('utf-8'))







