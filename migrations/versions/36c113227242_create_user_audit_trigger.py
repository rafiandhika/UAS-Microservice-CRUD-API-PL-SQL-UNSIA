"""Create user_audit_trigger

Revision ID: 36c113227242
Revises: 
Create Date: 2024-02-14 00:45:24.926601

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36c113227242'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('password', sa.LargeBinary(), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('authentication', sa.Boolean(), nullable=True),
    sa.Column('api_key', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('api_key'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('user_audit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('method', sa.String(length=10), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('old_username', sa.String(length=255), nullable=True),
    sa.Column('new_username', sa.String(length=255), nullable=True),
    sa.Column('old_email', sa.String(length=255), nullable=True),
    sa.Column('new_email', sa.String(length=255), nullable=True),
    sa.Column('old_first_name', sa.String(length=255), nullable=True),
    sa.Column('new_first_name', sa.String(length=255), nullable=True),
    sa.Column('old_last_name', sa.String(length=255), nullable=True),
    sa.Column('new_last_name', sa.String(length=255), nullable=True),
    sa.Column('log_time', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    op.execute('''
    CREATE OR REPLACE FUNCTION user_audit_trigger()
    RETURNS TRIGGER AS $$
    BEGIN
        IF TG_OP = 'INSERT' THEN
            INSERT INTO user_audit (method, user_id, new_username, new_email, new_first_name, new_last_name, log_time)
            VALUES ('INSERT', NEW.id, NEW.username, NEW.email, NEW.first_name, NEW.last_name, now());
            RETURN NEW;
        ELSIF TG_OP = 'UPDATE' THEN
            IF OLD.username != NEW.username OR OLD.email != NEW.email OR OLD.first_name != NEW.first_name OR OLD.last_name != NEW.last_name THEN
                INSERT INTO user_audit (method, user_id, 
                                         old_username, new_username, 
                                         old_email, new_email, 
                                         old_first_name, new_first_name, 
                                         old_last_name, new_last_name, 
                                         log_time)
                VALUES ('UPDATE', NEW.id, 
                        CASE WHEN OLD.username != NEW.username THEN OLD.username ELSE NULL END, 
                        CASE WHEN OLD.username != NEW.username THEN NEW.username ELSE NULL END, 
                        CASE WHEN OLD.email != NEW.email THEN OLD.email ELSE NULL END, 
                        CASE WHEN OLD.email != NEW.email THEN NEW.email ELSE NULL END, 
                        CASE WHEN OLD.first_name != NEW.first_name THEN OLD.first_name ELSE NULL END, 
                        CASE WHEN OLD.first_name != NEW.first_name THEN NEW.first_name ELSE NULL END, 
                        CASE WHEN OLD.last_name != NEW.last_name THEN OLD.last_name ELSE NULL END, 
                        CASE WHEN OLD.last_name != NEW.last_name THEN NEW.last_name ELSE NULL END, 
                        now());
            END IF;
            RETURN NEW;
        ELSIF TG_OP = 'DELETE' THEN
            INSERT INTO user_audit (method, user_id, old_username, old_email, old_first_name, old_last_name, log_time)
            VALUES ('DELETE', OLD.id, OLD.username, OLD.email, OLD.first_name, OLD.last_name, now());
            RETURN OLD;
        END IF;
    END;
    $$ LANGUAGE plpgsql;
    ''')

    op.execute('''
    CREATE TRIGGER user_audit_trigger
    AFTER INSERT OR UPDATE OR DELETE ON "user"
    FOR EACH ROW EXECUTE FUNCTION user_audit_trigger();
    ''')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('DROP TRIGGER user_audit_trigger ON "user"')
    op.execute('DROP FUNCTION user_audit_trigger()')
    op.drop_table('user_audit')
    op.drop_table('user')
    # ### end Alembic commands ###
