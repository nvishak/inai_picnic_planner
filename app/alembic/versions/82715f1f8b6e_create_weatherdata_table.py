"""create weatherdata table

Revision ID: 82715f1f8b6e
Revises: 7a22b37b0c90
Create Date: 2023-12-25 18:14:22.961715

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '82715f1f8b6e'
down_revision = '7a22b37b0c90'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('weatherdata',
    sa.Column('date', sa.DATE, nullable=False),
    sa.Column('hour_of_the_day', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('temperature_2m', sa.Float(), nullable=False),
    sa.Column('apparent_temperature', sa.Float(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False, autoincrement='auto'),
    sa.Column('precipitation_probability', sa.Float(), nullable=False),
    sa.Column('rain', sa.Float(), nullable=False),
    sa.Column('cloud_cover', sa.Float(), nullable=False),
    sa.Column('h5_index', sa.BigInteger(), nullable=False),
    sa.Column('h9_index', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

    op.create_index(op.f('ix_h5_index'), 'weatherdata', ['h5_index'])
    op.create_index(op.f('ix_h9_index'), 'weatherdata', ['h9_index'])
    op.create_index(op.f('ix_date'), 'weatherdata', ['date'])
    op.create_unique_constraint('uq_uniqueness', 'weatherdata', ['date', 'hour_of_the_day', 'h5_index', 'h9_index'])
    
def downgrade():
    op.drop_index(op.f('ix_h5_index'), table_name='weatherdata')
    op.drop_index(op.f('ix_h9_index'), table_name='weatherdata')
    op.drop_index(op.f('ix_date'), table_name='weatherdata')
    op.drop_constraint('uq_uniqueness', 'weatherdata')
    op.drop_table('weatherdata')
