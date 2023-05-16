import os
import decimal
import adapter

MATERIAL_TYPE = {
    "m"         : "MATERIAL",
    "cb"        : "CB",
    "component" : "COMPONENT",
}

PRICE_NAME = {
    "list"  : "LISTPRICE",
    "cost"  : "COSTPRICE",
    "web"   : "WEBPRICE",
    "sale"  : "SALESPRICE",
    "floor" : "FLOORPRICE",
    "coupon": "COUPONPRICE",
}

PRICE_RULE_NAME = {
    "web"   : "WEBPRICERULE",
    "saving": "INSTANTSAVINGRULE",
    "floor" : "FLOORPRICERULE",
    "coupon": "COUPONPRICERULE",
}

DEFAULT_PRICE_ADAPTER = adapter.StubPriceAdapter()
DEFAULT_CURRENCY = "USD"
NA = "NA"


class Material(object):
    def __init__(self, part_no, scenario_id = NA, price_adapter = DEFAULT_PRICE_ADAPTER, material_type = MATERIAL_TYPE["m"]):
        self.__part_no = part_no
        self.__scenario_id = scenario_id
        self.__price_rule_map = {}
        self.__price_map = {}
        self.__material_type = material_type
        self.__price_adapter = price_adapter

    def __str__(self):
        lst = []
        lst += ["({})".format(str(x)) for x in self.__price_rule_map.values() if x]
        lst += ["({})".format(str(x)) for x in self.__price_map.values() if x]
        return "{}: {}".format(self.get_part_no(), ", ".join(lst)) 

    def get_part_no(self):
        return self.__part_no

    def get_scenario_id(self):
        return self.__scenario_id

    def get_price(self, name):
        return self.__price_map[name] if name in self.__price_map else Price(name, 0)

    def add_price_rule(self, name, definition, related_cb = NA):
        rule = PriceRule(name, definition)
        self.__price_rule_map[name] = rule
        return self

    def add_price(self, name, amount, currency = DEFAULT_CURRENCY):
        price = Price(name, amount, currency)
        self.__price_map[name] = price
        return self

    def add_component(self, material):
        raise NotImplementedError("Only CB can add Component")

    def get_component(self, part_no):
        raise NotImplementedError("Only CB can get Component")

    def request_price(self):
        price_map = self.__price_adapter.request_price(self)
        [self.add_price(k, v["price"], v["currency"]) for (k, v) in price_map.items()]

class ConvenienceBundle(Material):
    def __init__(self, part_no, scenario_id = NA, price_adapter = DEFAULT_PRICE_ADAPTER):
        super().__init__(part_no, scenario_id, price_adapter, MATERIAL_TYPE["cb"])
        self.__components = {}

    def __str__(self):
        lst = []
        lst.append(super().__str__())
        lst += [str(x) for x in self.__components.values() if x]
        return os.linesep.join(lst)

    def add_component(self, material):
        self.__components[material.get_part_no()] = material
        return self

    def get_component(self, part_no):
        return self.__components[part_no] if part_no in self.__components else None

    def request_price(self):
        super().request_price()
        [c.request_price() for c in self.__components.values()]

class Component(Material):
    def __init__(self, part_no, scenario_id = NA, price_adapter = DEFAULT_PRICE_ADAPTER):
        super().__init__(part_no, scenario_id, price_adapter, MATERIAL_TYPE["component"])

class PriceRule(object):
    def __init__(self, name, definition, related_cb = NA):
        self.__name = name
        self.__definition = definition
        self.__related_cb = related_cb

    def __str__(self):
        return "{}: {}, {}".format(self.get_name(), self.get_definition(), self.get_related_cb())

    def get_name(self):
        return self.__name

    def get_definition(self):
        return self.__definition

    def get_related_cb(self):
        return self.__related_cb

class Price(object):
    def __init__(self, name, amount, currency = DEFAULT_CURRENCY):
        self.__name = name
        self.__amount = decimal.Decimal(amount).quantize(decimal.Decimal('1.00'))
        self.__currency = currency

    def __eq__(self, price):
        return self.get_amount() == price.get_amount() and self.get_currency() == price.get_currency()

    def __str__(self):
        return "{}: {}, {}".format(self.get_name(), self.get_amount(), self.get_currency())

    def get_name(self):
        return self.__name

    def get_amount(self):
        return self.__amount

    def get_currency(self):
        return self.__currency

def test_material():
    m = Material("m")
    m.add_price_rule("web", "-10") \
     .add_price_rule("saving", "-10%") \
     .add_price("p1", 10) \
     .add_price("p2", 3.2) \
     .add_price("p3", "5.3131")

    print(m)

def test_cb():
    cb1 = ConvenienceBundle("cb1")
    cb1.add_component(Component("c1")) \
       .add_component(Component("c2")) \
       .add_component(Component("c3"))

    cb2 = ConvenienceBundle("cb2")
    
    c1 = Component("c1")
    c1.add_price_rule("web", "-10") \
      .add_price("p1", 10)
    cb3 = ConvenienceBundle("cb3")
    cb3.add_component(c1) \
       .add_price_rule("web", "-10") \
       .add_price("p1", 10)

    print(cb1)
    print(cb2)
    print(cb3)

def test_price():
    price1 = Price("demo", "3.141")
    price2 = Price("demo", 3.143)
    price3 = Price("demo", 3.145)

    print(price1)
    print(price2)
    print(price3)

    assert(price1 == price2)
    assert(price1 != price3)

def test_request_price():
    cb = ConvenienceBundle("test-cb-1", "5")
    cb.add_component(Component("20K4S0E900", "5")) \
      .add_component(Component("81G20084US", "5"))
    
    cb.request_price()
    print(cb)

if __name__ == "__main__":
    test_material()
    test_cb()
    test_price()
    test_request_price()
