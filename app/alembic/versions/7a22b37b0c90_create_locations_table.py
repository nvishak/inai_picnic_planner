"""create locations table

Revision ID: 7a22b37b0c90
Revises: e2412789c190
Create Date: 2023-12-25 18:14:13.895823

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '7a22b37b0c90'
down_revision = 'e2412789c190'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('locations',
    sa.Column('country', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('state', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('district', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('zipcode', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False, autoincrement='auto'),
    sa.Column('locality', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('centroid_latitude', sa.Float(), nullable=False),
    sa.Column('centroid_longitude', sa.Float(), nullable=False),
    sa.Column('h5_index', sa.BigInteger(), nullable=False),
    sa.Column('h9_index', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_index(op.f('ix_h5_index'), 'locations', ['h5_index'])
    op.create_index(op.f('ix_h9_index'), 'locations', ['h9_index'])
    
def downgrade():
    op.drop_index(op.f('ix_h5_index'), table_name='locations')
    op.drop_index(op.f('ix_h9_index'), table_name='locations')
    op.drop_table('locations')
