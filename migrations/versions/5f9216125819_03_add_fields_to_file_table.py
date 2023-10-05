"""03_add_fields_to_file_table

Revision ID: 5f9216125819
Revises: 9dd1883bf706
Create Date: 2023-10-05 08:24:17.484458

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f9216125819'
down_revision: Union[str, None] = '9dd1883bf706'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('file', sa.Column('name', sa.String(length=255), nullable=False))
    op.add_column('file', sa.Column('path', sa.String(length=255), nullable=False))
    op.add_column('file', sa.Column('size', sa.Integer(), nullable=False))
    op.add_column('file', sa.Column('is_downloadable', sa.Boolean(), nullable=True))
    op.create_unique_constraint(None, 'file', ['path'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'file', type_='unique')
    op.drop_column('file', 'is_downloadable')
    op.drop_column('file', 'size')
    op.drop_column('file', 'path')
    op.drop_column('file', 'name')
    # ### end Alembic commands ###