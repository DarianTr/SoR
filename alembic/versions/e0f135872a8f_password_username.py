"""password/username

Revision ID: e0f135872a8f
Revises: ba19337b6c4f
Create Date: 2022-12-10 18:47:00.421142

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0f135872a8f'
down_revision = 'ba19337b6c4f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Schueler', sa.Column('username', sa.Text(), nullable=True))
    op.add_column('Schueler', sa.Column('password', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Schueler', 'password')
    op.drop_column('Schueler', 'username')
    # ### end Alembic commands ###
