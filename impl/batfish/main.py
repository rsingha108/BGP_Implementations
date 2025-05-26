# Import packages
import json
from utils import *
from startup import *
from typing import List, Optional  # noqa: F401
import pandas as pd
import time
from IPython.display import display
from pandas.io.formats.style import Styler
from pybatfish.client.session import Session  # noqa: F401
# noinspection PyUnresolvedReferences
from pybatfish.datamodel import Edge, Interface  # noqa: F401
from pybatfish.datamodel.answer import TableAnswer
from pybatfish.datamodel.flow import HeaderConstraints, PathConstraints  # noqa: F401
from pybatfish.datamodel.route import BgpRoute  # noqa: F401
from pybatfish.util import get_html
from pybatfish.datamodel.route import BgpRouteConstraints


# load the test
with open("test.json", "r") as f:
    test = json.load(f)

# Parse the route
route = test["route"]   

# Update rmap configuration
update_batfish_config(test["rmap"])

# Initialize Batfish session
bf = Session(host="localhost")
NETWORK_NAME = "example_network"
SNAPSHOT_NAME = "example_snapshot"
SNAPSHOT_PATH = "../networks/route-analysis"
bf.set_network(NETWORK_NAME)
bf.init_snapshot(SNAPSHOT_PATH, name=SNAPSHOT_NAME, overwrite=True)


# Create route for testing
asp = list(map(int,route["as-path"].split()))
com = route["community"]

inRoute1 = BgpRoute(network=route["prefix"], 
                    originatorIp="4.4.4.4", 
                    originType="egp", 
                    protocol="bgp",
                    asPath=asp, #[32,34],
                    communities=com, #["1:0", "22221:1"],
                    localPreference=int(route["local-pref"]),
                    metric=int(route["med"]),
                    nextHopIp="3.0.0.3")

# Test how our policy treats this route
result = bf.q.testRoutePolicies(policies="Rmap", 
                                direction="in", 
                                inputRoutes=[inRoute1]).answer().frame()

# Display the result
result.to_json("output.json", orient="records", indent=2)
with open("../networks/route-analysis/configs/border4.cfg", "r") as f:
    config = f.read()
with open("config.txt", "w") as f:
    f.write(config)

# Save the result to a file  
exp_decision = test["expected"]
router_decision = result["Action"][0].lower()

with open("result.txt", "w") as f:
    f.write(f"{exp_decision},{router_decision}")