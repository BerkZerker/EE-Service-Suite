"""add all models

Revision ID: initial_migration
Revises: 
Create Date: 2023-03-22 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'initial_migration'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('full_name', sa.String(length=100), nullable=True),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('role', sa.Enum('admin', 'technician', name='userrole'), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )
    
    # Create customers table
    op.create_table('customers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=True),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_customers_email'), 'customers', ['email'], unique=False)
    op.create_index(op.f('ix_customers_id'), 'customers', ['id'], unique=False)
    
    # Create parts table
    op.create_table('parts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(length=50), nullable=True),
        sa.Column('sku', sa.String(length=50), nullable=True),
        sa.Column('quantity', sa.Integer(), nullable=True),
        sa.Column('min_stock', sa.Integer(), nullable=True),
        sa.Column('reorder_point', sa.Integer(), nullable=True),
        sa.Column('cost_price', sa.Float(), nullable=False),
        sa.Column('retail_price', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_parts_id'), 'parts', ['id'], unique=False)
    op.create_index(op.f('ix_parts_sku'), 'parts', ['sku'], unique=True)
    
    # Create services table
    op.create_table('services',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_services_id'), 'services', ['id'], unique=False)
    
    # Create bikes table
    op.create_table('bikes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('specs', sa.Text(), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['customers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bikes_id'), 'bikes', ['id'], unique=False)
    
    # Create tickets table
    op.create_table('tickets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ticket_number', sa.String(length=20), nullable=False),
        sa.Column('problem_description', sa.Text(), nullable=False),
        sa.Column('diagnosis', sa.Text(), nullable=True),
        sa.Column('status', sa.Enum('intake', 'diagnosis', 'awaiting_parts', 'in_progress', 'complete', 'delivered', name='ticketstatus'), nullable=True),
        sa.Column('priority', sa.Enum('low', 'medium', 'high', 'urgent', name='ticketpriority'), nullable=True),
        sa.Column('estimated_completion', sa.DateTime(), nullable=True),
        sa.Column('bike_id', sa.Integer(), nullable=True),
        sa.Column('technician_id', sa.Integer(), nullable=True),
        sa.Column('labor_cost', sa.Float(), nullable=True),
        sa.Column('total_parts_cost', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['bike_id'], ['bikes.id'], ),
        sa.ForeignKeyConstraint(['technician_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tickets_id'), 'tickets', ['id'], unique=False)
    op.create_index(op.f('ix_tickets_ticket_number'), 'tickets', ['ticket_number'], unique=True)
    
    # Create ticket_parts table
    op.create_table('ticket_parts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ticket_id', sa.Integer(), nullable=True),
        sa.Column('part_id', sa.Integer(), nullable=True),
        sa.Column('quantity', sa.Integer(), nullable=True),
        sa.Column('price_charged', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['part_id'], ['parts.id'], ),
        sa.ForeignKeyConstraint(['ticket_id'], ['tickets.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ticket_parts_id'), 'ticket_parts', ['id'], unique=False)
    
    # Create ticket_updates table
    op.create_table('ticket_updates',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ticket_id', sa.Integer(), nullable=True),
        sa.Column('previous_status', sa.Enum('intake', 'diagnosis', 'awaiting_parts', 'in_progress', 'complete', 'delivered', name='ticketstatus'), nullable=True),
        sa.Column('new_status', sa.Enum('intake', 'diagnosis', 'awaiting_parts', 'in_progress', 'complete', 'delivered', name='ticketstatus'), nullable=False),
        sa.Column('note', sa.Text(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['ticket_id'], ['tickets.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ticket_updates_id'), 'ticket_updates', ['id'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index(op.f('ix_ticket_updates_id'), table_name='ticket_updates')
    op.drop_table('ticket_updates')
    op.drop_index(op.f('ix_ticket_parts_id'), table_name='ticket_parts')
    op.drop_table('ticket_parts')
    op.drop_index(op.f('ix_tickets_ticket_number'), table_name='tickets')
    op.drop_index(op.f('ix_tickets_id'), table_name='tickets')
    op.drop_table('tickets')
    op.drop_index(op.f('ix_bikes_id'), table_name='bikes')
    op.drop_table('bikes')
    op.drop_index(op.f('ix_services_id'), table_name='services')
    op.drop_table('services')
    op.drop_index(op.f('ix_parts_sku'), table_name='parts')
    op.drop_index(op.f('ix_parts_id'), table_name='parts')
    op.drop_table('parts')
    op.drop_index(op.f('ix_customers_id'), table_name='customers')
    op.drop_index(op.f('ix_customers_email'), table_name='customers')
    op.drop_table('customers')
    op.drop_table('users')