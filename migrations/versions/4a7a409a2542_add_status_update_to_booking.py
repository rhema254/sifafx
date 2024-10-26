"""Add status update to Booking

Revision ID: 4a7a409a2542
Revises: 
Create Date: 2024-10-23 00:27:10.050260

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4a7a409a2542'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bookings', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.String(length=10), nullable=False))
        batch_op.alter_column('id',
               existing_type=mysql.BIGINT(display_width=20, unsigned=True),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
        batch_op.alter_column('l_name',
               existing_type=mysql.VARCHAR(length=40),
               type_=sa.String(length=30),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.String(length=80),
               existing_nullable=False)
        batch_op.alter_column('timezone',
               existing_type=mysql.VARCHAR(length=50),
               type_=sa.String(length=30),
               existing_nullable=False)
        batch_op.alter_column('service',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.String(length=30),
               existing_nullable=False)
        batch_op.alter_column('meet_link',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.String(length=60),
               existing_nullable=True,
               existing_server_default=sa.text("'none'"))
        batch_op.alter_column('created_at',
               existing_type=mysql.TIMESTAMP(),
               type_=sa.DateTime(),
               nullable=True,
               existing_server_default=sa.text('current_timestamp()'))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bookings', schema=None) as batch_op:
        batch_op.alter_column('created_at',
               existing_type=sa.DateTime(),
               type_=mysql.TIMESTAMP(),
               nullable=False,
               existing_server_default=sa.text('current_timestamp()'))
        batch_op.alter_column('meet_link',
               existing_type=sa.String(length=60),
               type_=mysql.VARCHAR(length=255),
               existing_nullable=True,
               existing_server_default=sa.text("'none'"))
        batch_op.alter_column('service',
               existing_type=sa.String(length=30),
               type_=mysql.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.alter_column('timezone',
               existing_type=sa.String(length=30),
               type_=mysql.VARCHAR(length=50),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.String(length=80),
               type_=mysql.VARCHAR(length=255),
               existing_nullable=False)
        batch_op.alter_column('l_name',
               existing_type=sa.String(length=30),
               type_=mysql.VARCHAR(length=40),
               existing_nullable=False)
        batch_op.alter_column('id',
               existing_type=sa.Integer(),
               type_=mysql.BIGINT(display_width=20, unsigned=True),
               existing_nullable=False,
               autoincrement=True)
        batch_op.drop_column('status')

    # ### end Alembic commands ###