"""fix types

Revision ID: 8ffbae7b1c48
Revises: c486a7a791d3
Create Date: 2024-12-12 19:02:05.899110

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ffbae7b1c48'
down_revision: Union[str, None] = 'c486a7a791d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('apartment_info', schema='payment_management') as batch_op:
        batch_op.alter_column('common_square',
               existing_type=sa.INTEGER(),
               type_=sa.Float(),
               existing_comment='Общая площадь квартиры',
               existing_nullable=False)
        batch_op.alter_column('kitchen_square',
               existing_type=sa.INTEGER(),
               type_=sa.Float(),
               existing_comment='Площадь кухни',
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('apartment_info', schema='payment_management') as batch_op:
        batch_op.alter_column('kitchen_square',
               existing_type=sa.Float(),
               type_=sa.INTEGER(),
               existing_comment='Площадь кухни',
               existing_nullable=True)
        batch_op.alter_column('common_square',
               existing_type=sa.Float(),
               type_=sa.INTEGER(),
               existing_comment='Общая площадь квартиры',
               existing_nullable=False)

    # ### end Alembic commands ###