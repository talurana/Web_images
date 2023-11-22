"""update image with user_id

Revision ID: 32a49f838f30
Revises: 30026ba885a3
Create Date: 2023-11-05 18:35:51.433523

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '32a49f838f30'
down_revision: Union[str, None] = '30026ba885a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('image', sa.Column('edited_by', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'image', ['id'])
    op.create_foreign_key(None, 'image', 'user', ['edited_by'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'image', type_='foreignkey')
    op.drop_constraint(None, 'image', type_='unique')
    op.drop_column('image', 'edited_by')
    # ### end Alembic commands ###