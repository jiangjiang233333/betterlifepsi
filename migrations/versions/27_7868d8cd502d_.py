# encoding=utf-8
"""Add seed data, schema change for franchise support

Revision ID: 7868d8cd502d
Revises: 0051eed6ee5d
Create Date: 2016-07-22 21:36:05.852282

"""

# revision identifiers, used by Alembic.
revision = '7868d8cd502d'
down_revision = '0051eed6ee5d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    from sqlalchemy.sql import text
    # Organization
    op.add_column('organization', sa.Column('type_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'organization', 'enum_values', ['type_id'], ['id'])
    op.add_column('product', sa.Column('franchise_price', sa.Numeric(precision=8, scale=2, decimal_return_scale=2), nullable=True))
    op.get_bind().execute(text("INSERT INTO enum_values (type_id, code, display) VALUES (1, 'ORGANIZATION_TYPE', '组织类型');"))
    op.get_bind().execute(text("INSERT INTO enum_values (type_id, code, display) VALUES ((SELECT id FROM enum_values WHERE code='ORGANIZATION_TYPE'), 'DIRECT_SELLING_STORE', '直营店');"))
    op.get_bind().execute(text("INSERT INTO enum_values (type_id, code, display) VALUES ((SELECT id FROM enum_values WHERE code='ORGANIZATION_TYPE'), 'FRANCHISE_STORE', '加盟店');"))
    op.get_bind().execute(text("UPDATE organization set type_id = (SELECT id FROM enum_values WHERE code='DIRECT_SELLING_STORE')"))
    op.get_bind().execute(text("ALTER TABLE organization ALTER COLUMN type_id SET NOT NULL;"))

    # Purchase Order
    op.add_column('purchase_order', sa.Column('type_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'purchase_order', 'enum_values', ['type_id'], ['id'])
    op.get_bind().execute(text("INSERT INTO enum_values (type_id, code, display) values (1, 'PURCHASE_ORDER_TYPE', '采购单类型');"))
    op.get_bind().execute(text("INSERT INTO enum_values (type_id, code, display) values ((SELECT id FROM enum_values WHERE code='PURCHASE_ORDER_TYPE'), 'DIRECT_PURCHASE_ORDER', '直接采购单');"))
    op.get_bind().execute(text("INSERT INTO enum_values (type_id, code, display) values ((SELECT id FROM enum_values WHERE code='PURCHASE_ORDER_TYPE'), 'FRANCHISE_PURCHASE_ORDER', '加盟商采购单');"))
    op.get_bind().execute(text("UPDATE purchase_order set type_id = (SELECT id FROM enum_values WHERE code='DIRECT_PURCHASE_ORDER')"))
    op.get_bind().execute(text("ALTER TABLE purchase_order ALTER COLUMN type_id SET NOT NULL;"))

    # Sales order
    op.add_column('sales_order', sa.Column('type_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'sales_order', 'enum_values', ['type_id'], ['id'])
    op.get_bind().execute(text("INSERT INTO enum_values (type_id, code, display) values (1, 'SALES_ORDER_TYPE', '销售单类型');"))
    op.get_bind().execute(text("INSERT INTO enum_values (type_id, code, display) values ((SELECT id FROM enum_values WHERE code='SALES_ORDER_TYPE'), 'DIRECT_SALES_ORDER', '直接销售单');"))
    op.get_bind().execute(text("INSERT INTO enum_values (type_id, code, display) values ((SELECT id FROM enum_values WHERE code='SALES_ORDER_TYPE'), 'FRANCHISE_SALES_ORDER', '加盟商销售单');"))
    op.get_bind().execute(text("UPDATE sales_order set type_id = (SELECT id FROM enum_values WHERE code='DIRECT_SALES_ORDER')"))
    op.get_bind().execute(text("ALTER TABLE sales_order ALTER COLUMN type_id SET NOT NULL;"))

    # New inventory transaction type
    op.get_bind().execute(text("INSERT INTO enum_values (type_id, code, display) values ((SELECT id FROM enum_values WHERE code='INVENTORY_TRANSACTION_TYPE'), 'FRANCHISE_SALES_OUT', '加盟商销售出库');"))
    op.get_bind().execute(text("UPDATE enum_values set code='DIRECT_SALES_OUT', display='直接销售出库' WHERE code='SALES_OUT'"))

    # New role for manage sales order from FRANCHISE
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    from sqlalchemy.sql import text
    op.get_bind().execute(text("UPDATE enum_values set code='SALES_OUT', display='销售出库' WHERE code='DIRECT_SALES_OUT'"))
    op.get_bind().execute(text("DELETE FROM enum_values where code = 'FRANCHISE_SALES_OUT'"))

    # Sales Order
    op.drop_column('sales_order', 'type_id')
    op.get_bind().execute(text("DELETE FROM enum_values where code in ('SALES_ORDER_TYPE', 'DIRECT_SALES_ORDER', 'FRANCHISE_SALES_ORDER')"))

    # Purchase Order
    op.drop_column('purchase_order', 'type_id')
    op.get_bind().execute(text("DELETE FROM enum_values where code in ('PURCHASE_ORDER_TYPE', 'DIRECT_PURCHASE_ORDER', 'FRANCHISE_PURCHASE_ORDER')"))

    # Organization
    op.drop_column('organization', 'type_id')
    op.get_bind().execute(text("DELETE FROM enum_values where code in ('ORGANIZATION_TYPE', 'DIRECT_SELLING_STORE', 'FRANCHISE_STORE')"))

    # Drop franchise_price field
    op.drop_column('product', 'franchise_price')
    ### end Alembic commands ###
