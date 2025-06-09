"""create stores and items table

Revision ID: af43c7c60d90
Revises: 
Create Date: 2025-01-03 16:55:51.925042

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'af43c7c60d90'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.execute("""CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    users TEXT NOT NULL UNIQUE,
                    address TEXT,
                    contact_number TEXT,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL);""")

def downgrade() -> None:
    op.execute("DROP TABLE stores;")
