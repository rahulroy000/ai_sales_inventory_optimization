import pandas as pd                   # Import use librari

pd.set_option("display.max_rows", None)     # Show all rows
pd.set_option("display.max_columns", None)  # Show all Columns

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

# df.info()                                 # Show all Info in Data & NON Value

# __________________________________________________________________________________________________________________________________________ #
# Display summary statistics for all columns in the DataFrame
# Includes count, unique, mean, standard deviation, minimum, maximum, etc.

# print(df.describe(include="all").T)

# describe(include="all") -> Summarizes all columns, including text and numeric columns
# .T                  -> Transposes the table (swaps rows and columns)
# print()             -> Displays the result in the terminal
# __________________________________________________________________________________________________________________________________________ #

# print(df.isnull())            # Show Defualt Null Value
# print(df.isnull().head(100))  # Show Pass Value Null Value
# print(df.isnull().sum())      # Sum all Null Value

missing = df.isnull().sum()     # Store all null Value in Variable
print(missing[missing > 0])

# missing_percent = (df.isnull().mean() * 100).round(2)
# print(missing_percent[missing_percent > 0])