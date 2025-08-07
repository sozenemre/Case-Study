import os
import sys
from datetime import datetime, timezone
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import psycopg2
from dotenv import load_dotenv

class ClansETL:

    def __init__(self, db_config):
        self.db_config = db_config

    def extract(self) -> pd.DataFrame:
        file_path = os.path.join(os.path.dirname(__file__), "clan_sample_data.csv")
        df = pd.read_csv(file_path)
        return df

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        
        data["created_at"] = data["created_at"].apply(
            lambda val: datetime(1970, 1, 1)
            if pd.isna(val) or str(val).strip() == ""
            else datetime.fromtimestamp(int(val), tz=timezone.utc)
            if str(val).isdigit() and len(str(val)) >= 10
            else pd.to_datetime(val, errors='coerce') or datetime(1970, 1, 1)
        )
        data["created_at"] = data["created_at"].fillna(datetime(1970, 1, 1))

        data["region"] = data["region"].apply(
            lambda x: x if isinstance(x, str) and len(x) == 2 and x.isalpha() else "ZZ"
        )

        return data

    def load(self, data: pd.DataFrame):
        conn = psycopg2.connect(**self.db_config)
        cur = conn.cursor()

        insert_query = """
            INSERT INTO clans (name, region, created_at)
            VALUES (%s, %s, %s)
        """

        rows = data[["name", "region", "created_at"]].values.tolist()

        try:
            cur.executemany(insert_query, rows)
            conn.commit()
            print(f"[ClansETL] Loaded {len(rows)} rows into 'clans' table.")
        except Exception as e:
            conn.rollback()
            print(f"[ClansETL] Error loading data: {e}")
            raise
        finally:
            cur.close()
            conn.close()

    def run(self):
        df = self.extract()
        df = self.transform(df)
        self.load(df)


if __name__ == "__main__":
    
    load_dotenv()
    
    db_config = {
        "host": os.getenv("DB_HOST"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "database": os.getenv("DB_NAME")
    }
    job = ClansETL(db_config=db_config)
    job.run()