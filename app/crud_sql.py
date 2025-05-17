from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import text

from app.connect_postgres import get_session

session = get_session()

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