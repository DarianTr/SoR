"""relationshipErweiterung

Revision ID: e00374e14f68
Revises: 90725eede50c
Create Date: 2022-12-05 23:22:49.307348

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e00374e14f68'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('schueler', sa.Column('zweitwunsch', mysql.INTEGER(display_width=10), nullable=True))
    op.add_column('schueler', sa.Column('drittwunsch', mysql.INTEGER(display_width=10), nullable=True))
    op.add_column('schueler', sa.Column('projekt', mysql.INTEGER(display_width=10), nullable=True))
    op.create_foreign_key(None, 'schueler', 'workshop', ['projekt'], ['id'])
    op.create_foreign_key(None, 'schueler', 'workshop', ['zweitwunsch'], ['id'])
    op.create_foreign_key(None, 'schueler', 'workshop', ['drittwunsch'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'schueler', type_='foreignkey')
    op.drop_constraint(None, 'schueler', type_='foreignkey')
    op.drop_constraint(None, 'schueler', type_='foreignkey')
    op.drop_column('schueler', 'projekt')
    op.drop_column('schueler', 'drittwunsch')
    op.drop_column('schueler', 'zweitwunsch')
    # ### end Alembic commands ###
