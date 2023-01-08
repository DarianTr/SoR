"""relationship\

Revision ID: 5308f978180d
Revises: e00374e14f68
Create Date: 2022-12-05 23:57:33.649806

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5308f978180d'
down_revision = 'e00374e14f68'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_Schueler_projekt'), 'Schueler', ['projekt'], unique=False)
    op.drop_constraint('Schueler_ibfk_2', 'Schueler', type_='foreignkey')
    op.drop_constraint('Schueler_ibfk_3', 'Schueler', type_='foreignkey')
    op.drop_constraint('Schueler_ibfk_1', 'Schueler', type_='foreignkey')
    op.drop_column('Schueler', 'zweitwunsch')
    op.drop_column('Schueler', 'drittwunsch')
    op.drop_column('Schueler', 'erstwunsch')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Schueler', sa.Column('erstwunsch', mysql.VARCHAR(length=255), nullable=True))
    op.add_column('Schueler', sa.Column('drittwunsch', mysql.VARCHAR(length=255), nullable=True))
    op.add_column('Schueler', sa.Column('zweitwunsch', mysql.VARCHAR(length=255), nullable=True))
    op.create_foreign_key('Schueler_ibfk_1', 'Schueler', 'Workshop', ['erstwunsch'], ['name'])
    op.create_foreign_key('Schueler_ibfk_3', 'Schueler', 'Workshop', ['zweitwunsch'], ['name'])
    op.create_foreign_key('Schueler_ibfk_2', 'Schueler', 'Workshop', ['drittwunsch'], ['name'])
    op.drop_index(op.f('ix_Schueler_projekt'), table_name='Schueler')
    # ### end Alembic commands ###