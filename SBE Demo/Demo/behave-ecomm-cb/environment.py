import re
import sys
sys.path.append("steps")

import adapter

PRICE_ADAPTER_POOL = {
    "ecomm": adapter.EcommPriceAdapter(),
    "mock": adapter.MockPriceAdapter(),
    "stub": adapter.StubPriceAdapter(),
}

# ------------------------------------------------------------------------------
# you may change the adapter name here to select proper one you need, 
# and DON'T touch other things
PRICE_ADAPTER = PRICE_ADAPTER_POOL["mock"]
# ------------------------------------------------------------------------------

def before_feature(context, feature):
    print("[INFO] Price adapter is {}".format(PRICE_ADAPTER.__class__.__name__))
    context.price_adapter = PRICE_ADAPTER

def before_scenario(context, scenario):
    context.cb = {}
    context.components_not_in_cb = {}
    context.scenario_id = re.match("\[(.*?)].*", scenario.name).group(1)