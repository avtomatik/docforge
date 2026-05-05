#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 20:50:18 2025

@author: alexandermikhailov
"""

from datetime import date
from pathlib import Path
from zipfile import ZipFile

import pandas as pd
import yaml
from mailmerge import MailMerge

from core.config import settings
from core.enums import Data, Template
from core.paths import DATA_DIR
from core.works import Work


def business_logic(df: pd.DataFrame) -> pd.DataFrame:
    """Update for More Refined Business Logic"""
    return df


def generate_file_name(template: Template, fields: dict, index: int) -> str:
    today = date.today()

    amount = fields["net_amount"]
    document_number = fields["document_number"]

    MAP = {
        Template.ACT: f"Contract {settings.PARTNER_NAME} Act {fields['inception_date']:%Y-%m}.docx",
        Template.ADDENDUM: (
            f"{settings.REF_PLACEHOLDER} Addendum {document_number:04n}-{today}.docx"
        ),
        Template.COVER_NOTE: f"{fields['account_name']} {fields['inception_date']:%Y} Cover Note.docx",
        Template.DEBIT_NOTE: (
            f"{settings.REF_PLACEHOLDER} "
            f'{"Debit" if amount >= 0 else "Advice"} Note '
            f"{document_number:06n}"
            f'{"PRM" if amount >= 0 else "RPM"}.docx'
        ),
        Template.ENDORSEMENT: (
            f"{settings.REF_PLACEHOLDER} Endorsement {document_number:04n}-"
            f"{index:04n}.docx"
        ),
        Template.LETTER: f"{fields['account_name']} {fields['document_date']:%Y} Official Letter.docx",
        Template.LETTER_0x9: f"{fields['umr']:} {fields['document_date']:%Y} 0x9.docx",
        Template.LETTER_CEM: f"{fields['account_name']} {fields['document_date']:%Y} CEM.docx",
        Template.LETTER_FIRM_ORDER: (
            f"{fields['account_name']} {fields['document_date']:%Y} Firm Order Response.docx"
        ),
        Template.LETTER_WARRANTY: f"{fields['umr']} {fields['document_date']:%Y} Warranty Letter.docx",
        Template.NDA: "to_do.docx",
        Template.SCOPES: f"Contract {settings.PARTNER_NAME} Scopes {fields['inception_date']:%Y-%m}.docx",
        Template.SERVICES_ACT: (
            f"Services Act {fields['broker']} "
            f"{fields['inception_date']:%Y-%m}-{document_number:04n}.docx"
        ),
        Template.SLIP: f"{fields['account_name']} {fields['inception_date']:%Y} Slip {fields['underwriter']}.docx",
        Template.SLIP_TREATY: (
            f"{settings.ACCOUNT_NAME} Primary Treaty {settings.REF_RESERVED} {fields['inception_date']:%Y} "
            f"Endorsement {document_number:04n} "
            f"{fields['underwriter']}.docx"
        ),
        Template.SPECIAL_ACCEPTANCE: (
            f"{settings.REF_PLACEHOLDER} Special Acceptance {document_number:04n}.docx"
        ),
    }

    return MAP.get(template, "default.docx")


def generate_string_panel(file_path: Path, two_columned: bool = False) -> list:
    df = pd.read_excel(file_path)

    panel = []

    for _, row in df.iterrows():
        formatted_row = row.copy()
        formatted_row.iloc[-1] = f"{row.iloc[-1]:.7%}"
        if two_columned:
            formatted_row.iloc[-2] = f"-\xa0{row.iloc[-2]};"
        panel.append(formatted_row.iloc[-2:].to_dict())

    return panel


def transform_stringify(df: pd.DataFrame) -> pd.DataFrame:
    datetime_columns = df.select_dtypes(include="datetime64").columns
    float_columns = df.select_dtypes(include="float64").columns
    int_columns = df.select_dtypes(include="int64").columns

    for column in datetime_columns:
        df.loc[:, column] = df.loc[:, column].apply(
            lambda _: f'{_:%d\xa0%B\xa0%Y}'
        )

    for column in float_columns:
        # =====================================================================
        # For Monetary Values
        # =====================================================================
        df.loc[:, column] = df.loc[:, column].apply(lambda _: f"{_:,.2f}")
        # # ===================================================================
        # # For Percentage Values
        # # ===================================================================
        # df.loc[:, column] = df.loc[:, column].apply(lambda _: f"{_:.4%}")

    for column in int_columns:
        # =====================================================================
        # For Serial Numbers
        # =====================================================================
        df.loc[:, column] = df.loc[:, column].apply(lambda _: f"{_:04n}")

    for column in ["ref"]:
        df.loc[:, column] = df.loc[:, column].apply(
            lambda _: f"{settings.PREFIX}{_}"
        )

    return df


def write_to_disk(
    work: Work, fields: dict, map_fields: dict[str, str], index: int
) -> None:
    if settings.ARCHIVE_NAME is None:
        template_path = work.path_src / work.template.template_name
    else:
        template_path = ZipFile(work.path_src / settings.ARCHIVE_NAME).open(
            work.template.template_name
        )
    with MailMerge(template_path) as document:
        document.merge(**map_fields)

        if "cover_note" in work.template.template_name:
            document.merge_rows(
                settings.MERGE_ANCHOR,
                generate_string_panel(
                    file_path=DATA_DIR / settings.FILE_NAME_PANELS
                ),
            )
        if work.template.template_name == Template.LETTER_WARRANTY:
            document.merge_rows(
                settings.MERGE_ANCHOR,
                generate_string_panel(
                    file_path=DATA_DIR / settings.FILE_NAME_PANELS
                ),
            )
        if work.template.template_name == Template.LETTER_0x9:
            document.merge_rows(
                settings.MERGE_ANCHOR,
                generate_string_panel(
                    file_path=DATA_DIR / settings.FILE_NAME_PANELS,
                    two_columned=True,
                ),
            )

        document.write(
            work.path_dst / generate_file_name(work.template, fields, index)
        )


def load_config(config_path: Path):
    with config_path.open() as f:
        return yaml.safe_load(f)


def create_work_from_config(work_config):
    # =========================================================================
    # TODO: Check If Making This a Method of Class
    # =========================================================================
    return Work(
        work_config["rows"],
        work_config["data_dir"],
        work_config["dst_path"],
        Data[work_config["data_source"]],
        Template[work_config["template"]],
    )


def extract_fields(row):
    return {
        "broker": row["broker"],
        "umr": row["umr"],
        "account_name": row["account_name"],
        "document_number": row["document_number"],
        "document_date": row["document_date"],
        "inception_date": row["inception_date"],
        "underwriter": row["underwriter"],
        "net_amount": row["net_amount"],
    }
