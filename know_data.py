import pandas as pd                   # Import use librari

df = pd.read_csv("data/raw/data.csv")               # Load CSV Data
# print("Here all 10 Rows and 10 Collm Data Info")
# print(df)                                         # Show 10 Columns and 10 rows

# print(df.head())                      # Show Defualt First 5 Rows
# print(df.head(10))                    # Show Defualt Last Pass Value Rows
# print(df.tail())                      # Show Defualt Last 5 Rows
# print(df.tail(10))                    # Show Defualt Last Pass Value Rows

# print(df.shape)                           # Show all Rows & Columns
# print("Rows:", df.shape[0])               # Show all Rows 
# print("Columns:", df.shape[1])            # Show all Columns

# print(df.columns.tolist())                # Show list Format Columns Names