from alembic import context
from sqlalchemy import create_engine

db_url = context.get_x_argument(as_dictionary=True).get('db_url', 'sqlite:///stores.db')

engine = create_engine(db_url)

with engine.connect() as connection:
    context.configure(connection=connection)

    with context.begin_transaction():
        context.run_migrations()