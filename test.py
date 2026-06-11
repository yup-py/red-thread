import pandas as pd

# Load your dataset
df = pd.read_csv("shows+casts+platform+score+budget+genre\streaming_catalog.csv")

# View unique values in the 'Platform' column
unique_platforms = df['platform'].unique()
print(unique_platforms)