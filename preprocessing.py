import pandas as pd

df = pd.read_csv("novel_data.csv")

df_desc = df["Description"]

print(df_desc)
