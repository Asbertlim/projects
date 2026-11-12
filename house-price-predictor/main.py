import pandas as pd

data = pd.read_csv("")
data = data.drop_duplicates()

print(data.tail())
