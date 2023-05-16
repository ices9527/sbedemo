import decimal
from engine import *

def __create_material(context, material_type, part_no, list_price, cost_price, web_price_rule, instant_saving_price_rule, related_cb, floor_price_rule, coupon_price_rule):
    if material_type == MATERIAL_TYPE["cb"]:
        material = ConvenienceBundle(part_no, context.scenario_id, context.price_adapter)
    else:
        material = Component(part_no, context.scenario_id, context.price_adapter)

    material.add_price(PRICE_NAME["list"], list_price) \
            .add_price(PRICE_NAME["cost"], cost_price) \
            .add_price_rule(PRICE_RULE_NAME["web"], web_price_rule) \
            .add_price_rule(PRICE_RULE_NAME["saving"], instant_saving_price_rule, related_cb) \
            .add_price_rule(PRICE_RULE_NAME["floor"], floor_price_rule) \
            .add_price_rule(PRICE_RULE_NAME["coupon"], coupon_price_rule)

    return material

def __verify_price(material, expect_price_map):
    for k, v in expect_price_map.items():
        result = material.get_price(PRICE_NAME[k])
        assert(v == result), "expect: {}, result: {}".format(v, result)

@given(u'Part No is {part_no}, Belonged CB is {belonged_cb}, Quantity is {quantity:d}, List Price is {list_price}, Cost Price is {cost_price}, Web Price Rule is {web_price_rule}, Instant Saving Price Rule is {instant_saving_price_rule}, Related CB is {related_cb}, Floor Price Rule is {floor_price_rule}, Coupon Price Rule is {coupon_price_rule}')
def step_impl(context, part_no, belonged_cb, quantity, list_price, cost_price, web_price_rule, instant_saving_price_rule, related_cb, floor_price_rule, coupon_price_rule):

    if part_no == belonged_cb:
        context.cb[part_no] = __create_material(context, MATERIAL_TYPE["cb"], part_no, list_price, cost_price, web_price_rule, instant_saving_price_rule, related_cb, floor_price_rule, coupon_price_rule)
        return

    for i in range(quantity):
        material = __create_material(context, MATERIAL_TYPE["component"], part_no, list_price, cost_price, web_price_rule, instant_saving_price_rule, related_cb, floor_price_rule, coupon_price_rule)

        if belonged_cb in context.cb:
            context.cb[belonged_cb].add_component(material)
        else:
            context.components_not_in_cb[part_no] = material

@when(u'Action is Add {part_no} to cart')
def step_impl(context, part_no):
    context.cb[part_no].request_price()

@then(u'{part_no}: Web Price is {expect_web_price}, Sale Price is {expect_sale_price}, Floor Price is {expect_floor_price}, Coupon Price is {expect_coupon_price}, Floor Price Violated by Sale Price is {expect_sale_price_violated}, Floor Price Violated by Coupon Price is {expect_coupon_price_violated}')
def step_impl(context, part_no, expect_web_price, expect_sale_price, expect_floor_price, expect_coupon_price, expect_sale_price_violated, expect_coupon_price_violated):
    expect_price_map = {
        "web": Price(PRICE_NAME["web"], expect_web_price),
        "sale": Price(PRICE_NAME["sale"], expect_sale_price),
        "floor": Price(PRICE_NAME["floor"], expect_floor_price),
        "coupon": Price(PRICE_NAME["coupon"], expect_coupon_price),
    }
    
    for k, cb in context.cb.items():
        if part_no == k:
            __verify_price(cb, expect_price_map)
            return
        else:
            component = cb.get_component(part_no)
            if component:
                __verify_price(component, expect_price_map)
                return

    if part_no in context.components_not_in_cb:
        __verify_price(context.components_not_in_cb[part_no], expect_price_map)
    else:
        assert(False), "Component must be verified"