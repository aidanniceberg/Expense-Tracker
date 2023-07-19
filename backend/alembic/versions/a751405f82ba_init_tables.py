"""init tables

Revision ID: a751405f82ba
Revises: 
Create Date: 2023-07-18 21:36:22.917572

"""
from alembic import op
import sqlalchemy as sa

from components.db import get_engine
from components.models.orm_models import Base


# revision identifiers, used by Alembic.
revision = 'a751405f82ba'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    engine = get_engine()
    Base.metadata.create_all(engine)


def downgrade() -> None:
    pass
