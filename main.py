import pandas as pd

df = pd.read_csv("data.csv")
print(len(df))
id_column = df['artifact_id']
for id in id_column:
    print(id)
