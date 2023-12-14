"""create file upload table

Revision ID: 53ea763b91d3
Revises: 91979b40eb38
Create Date: 2023-12-08 22:40:08.635119-05:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53ea763b91d3'
down_revision = '91979b40eb38'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
    "file_upload",
    sa.Column("course_id", sa.String(30), nullable=False),
    sa.Column("course_name", sa.String(100)),
    sa.Column("week_number", sa.String(10)),
    sa.Column("lecture_number", sa.String(10)),
    sa.Column("lecture_title", sa.String(200)),
    sa.Column("source_url", sa.String(2000)),
    sa.Column("s3_url", sa.String(2000), primary_key=True),
    sa.Column("file_name", sa.String(255)),
    sa.Column("doc_type", sa.String(10)),
    sa.Column("file_md5", sa.String(32)),
    )


def downgrade():
    op.drop_table("file_upload")

