"""empty message

Revision ID: 9f08a1b950ae
Revises: 4cd216f6bebe
Create Date: 2020-12-24 03:59:47.719882

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f08a1b950ae'
down_revision = '4cd216f6bebe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('miband4_devices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('serial', sa.String(length=12), nullable=True),
    sa.Column('software_revision', sa.String(length=10), nullable=True),
    sa.Column('hardware_revision', sa.String(length=10), nullable=True),
    sa.Column('mac_address', sa.String(length=17), nullable=False),
    sa.Column('auth_key', sa.String(length=32), nullable=False),
    sa.Column('last_fetch_data_timestamp', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('serial'),
    schema='miband_api'
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hashed', sa.LargeBinary(), nullable=False),
    sa.Column('password_salt', sa.LargeBinary(), nullable=False),
    sa.Column('fullname', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    schema='user_api'
    )
    op.create_table('activity_records',
    sa.Column('band_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
    sa.Column('category', sa.Integer(), nullable=True),
    sa.Column('intensity', sa.Integer(), nullable=True),
    sa.Column('steps', sa.Integer(), nullable=True),
    sa.Column('heartrate', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['band_id'], ['miband_api.miband4_devices.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user_api.users.id'], ),
    sa.PrimaryKeyConstraint('band_id', 'timestamp', 'user_id'),
    schema='miband_api'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('activity_records', schema='miband_api')
    op.drop_table('users', schema='user_api')
    op.drop_table('miband4_devices', schema='miband_api')
    # ### end Alembic commands ###
