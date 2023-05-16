import os
import json
import codecs
import requests
import interface

MSA_URL = {
    "rap2": "http://rap2api.taobao.org/app/mock/224822", #"http://rap2api.taobao.org/repository/get?id=224822", #,
    "ecomm": "http://service-price.sit.online.lenovo.com",
}

MSA_URI = {
    "getprice": {
        "rap2": "getPrice",
        "ecomm": "api/v1/price/getPrice",
    }
}

class EcommPriceAdapter(interface.PriceAdapter):
    def request_price(self, material, context = "US|B2C|usweb|EN"):
        url = "{}/{}".format(MSA_URL["ecomm"], MSA_URI["getprice"]["ecomm"])
        
        payload = {"productCodes": material.get_part_no(), "contextString": context}
        response = requests.get(url, params=payload)
        return json.loads(response.text)[material.get_part_no()]

class MockPriceAdapter(interface.PriceAdapter):
    def request_price(self, material, context = None):
        # FIXME
        # mock server is built on RAP2 at http://rap2.taobao.org/repository/editor?id=224822
        # RAP2 doesn't support different response with various parameter
        # it need to create multiple api to simulate query with parameter
        url = "{}/{}/{}".format(MSA_URL["rap2"], MSA_URI["getprice"]["rap2"], material.get_part_no())
        response = requests.get(url)
        print(response.text)
        return json.loads(response.text)[material.get_part_no()]

class StubPriceAdapter(interface.PriceAdapter):
    def request_price(self, material, context = None):
        steps_dir = os.path.dirname(os.path.abspath(__file__))
        home_dir = os.path.dirname(steps_dir)
        price_json_filename = os.path.join(home_dir, "testdata", "getPrice_{}_{}.json".format(material.get_part_no(), material.get_scenario_id()))

        with codecs.open(price_json_filename, "r", "utf-8") as price_file:
            return json.load(price_file)[material.get_part_no()]

class StubMaterial(object):
    def __init__(self, part_no, scenario_id = "NA"):
        self.__part_no = part_no
        self.__scenario_id = scenario_id

    def get_part_no(self):
        return self.__part_no

    def get_scenario_id(self):
        return self.__scenario_id

def test_stub():
    adapter = StubPriceAdapter()
    material = StubMaterial("20K4S0E900", "5")
    print(adapter.request_price(material))

def test_mock():
    adapter = MockPriceAdapter()
    material = StubMaterial("20K4S0E900", "5")
    print(adapter.request_price(material))

def test_ecomm():
    adapter = EcommPriceAdapter()
    material = StubMaterial("20K4S0E900", "5")
    print(adapter.request_price(material))

if __name__ == "__main__":
    #test_stub()
    test_mock()
    #test_ecomm()
