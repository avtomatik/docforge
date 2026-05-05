import pandas as pd
import psycopg2

from core.config import Settings
from core.enums import Data


def fetch_data(
    settings: Settings, data_source: Data, limit: int = None
) -> pd.DataFrame:
    query = f"SELECT * FROM {data_source.table_name}"
    if limit:
        query += f" LIMIT {limit}"

    with psycopg2.connect(settings.db_url) as conn:
        return pd.read_sql(query, conn)
