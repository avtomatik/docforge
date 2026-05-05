from api.schemas.placements import Placement
from core.db import get_connection


def get_placements(limit: int | None = None) -> list[Placement]:
    query = "SELECT * FROM placement"
    if limit:
        query += f" LIMIT {limit}"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            cols = [desc[0] for desc in cur.description]

    return [Placement(**dict(zip(cols, row))) for row in rows]
