import pandas as pd
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import text

from connect_postgres import get_session

session = get_session()


def insert_data(path, columns, table):
    df = pd.read_csv(path, names=columns).convert_dtypes()
    list_dict = df.to_dict(orient='records')

    session.bulk_insert_mappings(table, list_dict)
    session.commit()
    session.close()

def upsert_data(model, records, unique_constraint):
    stmt = insert(model).values(records)
    update_columns = {col.name: stmt.excluded[col.name]
                      for col in model.__table__.columns
                      if col.name != unique_constraint}

    upsert_stmt = stmt.on_conflict_do_update(
        index_elements=[unique_constraint],
        set_=update_columns
    )

    session.execute(upsert_stmt)
    session.commit()
    session.close()


def query_data(query):
    query = text(query)
    result = session.execute(query).fetchall()
    session.close()

    return result