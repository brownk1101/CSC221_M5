""" file to test functions in model_vetdb.py """

import pandas as pd
from model_vetdb import calculate_charges


data = {
    'PetName': ['Fluffy', 'Fluffy', 'Spike'],
    'Charge': [100, 200, 150]
}
df = pd.DataFrame(data)
result = calculate_charges(df)
assert result[0] == {'Fluffy': 300, 'Spike': 150}
assert result[1] == 450
assert result[2] == 225.0

print("All tests passed!")
