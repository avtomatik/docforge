#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 21:43:23 2023

@author: green-machine
"""

from core.config import settings
from core.db import fetch_data
from core.funcs import (business_logic, create_work_from_config,
                        extract_fields, load_config, transform_stringify,
                        write_to_disk)
from core.paths import BASE_DIR
from core.works import Work


def main(work: Work) -> None:
    df = fetch_data(settings, work.data_source, limit=work.num).pipe(
        business_logic
    )
    df_formatted = df.copy().pipe(transform_stringify)

    # =========================================================================
    # Main Loop
    # =========================================================================
    for index, row in df_formatted.iterrows():
        # =====================================================================
        # Populate Fields' Map
        # =====================================================================
        fields = extract_fields(row)
        map_fields = dict(row) | {"": ""}

        # =====================================================================
        # Write to Disk
        # =====================================================================
        write_to_disk(work, fields, map_fields, index)


if __name__ == "__main__":
    config = load_config(BASE_DIR / "config.yml")

    for work_config in config["works"]:
        work = create_work_from_config(work_config)
        main(work)
