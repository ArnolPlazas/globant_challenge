import pandas as pd


def get_records_from_file(path, columns):
    df = pd.read_csv(path, names=columns).convert_dtypes()
    records = df.to_dict(orient="records")

    return records