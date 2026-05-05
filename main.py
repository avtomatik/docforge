#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 21:43:23 2023

@author: green-machine
"""

from core.funcs import (create_work_from_config, extract_fields_from_domain,
                        load_config, write_to_disk)
from core.paths import BASE_DIR
from core.repositories.placement_repo import get_placements
from core.works import Work


def main(work: Work) -> None:
    placements = get_placements(limit=work.num)

    for index, placement in enumerate(placements):
        fields = extract_fields_from_domain(placement)

        write_to_disk(work, fields, fields, index)


if __name__ == "__main__":
    config = load_config(BASE_DIR / "config.yml")

    for work_config in config["works"]:
        work = create_work_from_config(work_config)
        main(work)
