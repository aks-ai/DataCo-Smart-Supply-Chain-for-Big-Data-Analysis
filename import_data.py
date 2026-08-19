import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load the secret variables from the .env file
load_dotenv()

# Securely grab the password
db_password = os.getenv("DB_PASSWORD")

# 1. Extract
print("Loading CSV...")
df = pd.read_csv("dataset/DataCoSupplyChainDataset.csv", encoding="ISO-8859-1")

# 2. Transform (Clean Column Names)
print("Cleaning column names...")
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("(", "")
    .str.replace(")", "")
)

# 3. Connect (Using the hidden password variable)
# Notice the 'f' before the string and the {db_password} in brackets
engine = create_engine(f"mysql+pymysql://root:{db_password}@localhost:3306/supply_chain_db")

# 4. Load
print("Pushing 180,000+ records to MySQL. This may take a minute...")
df.to_sql("orders", con=engine, if_exists="replace", index=False)

print("Success! Data is now in your local database.")