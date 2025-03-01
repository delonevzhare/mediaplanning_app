"""Добавили переменную plan_number в MediaPlan

Revision ID: 86e8c1f591e3
Revises: ee52130cf2d2
Create Date: 2024-07-10 12:56:19.313879

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86e8c1f591e3'
down_revision = 'ee52130cf2d2'
branch_labels = None
depends_on = None


def upgrade():
    # Step 1: Add the new column with a default value
    op.add_column('media_plan', sa.Column('plan_number', sa.Integer(), nullable=True, server_default='0'))

    # Step 2: Update the default value for existing rows
    op.execute('UPDATE media_plan SET plan_number = id')

    # Step 3: Alter the column to be NOT NULL
    op.alter_column('media_plan', 'plan_number', nullable=False, server_default=None)


def downgrade():
    op.drop_column('media_plan', 'plan_number')