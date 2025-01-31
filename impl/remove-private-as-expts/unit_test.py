from utils import *
import os

## Test Case 1
# combination_to_configs((True, True, None, False, None, False, "remove-private-AS all replace-AS"))

## Test Case 2
# combination_to_configs((True, False, True, True, None, False, "remove-private-AS all"))

## Test Case 3
# combination_to_configs((False, True, False, False, True, False, "remove-private-AS all"))

## Test Case 4
# combination_to_configs((True, True, True, False, True, True, "remove-private-AS all replace-AS"))

## Test Case 5
# combination_to_configs((False, True, None, False, True, False, "remove-private-AS all replace-AS"))


combination_to_configs((True, True, None, True, None, False, "remove-private-AS all replace-AS"))

os.system("bash run.sh")