from datetime import datetime
import pandas as pd
import re


def handle_spreadsheet(path_planilha: str) -> pd.DataFrame:
    return pd.read_excel(path_planilha, keep_default_na=False)


if __name__ == "__main__":
    file = "teste.xlsx"
    df = handle_spreadsheet(path_planilha=file)
    print(df)