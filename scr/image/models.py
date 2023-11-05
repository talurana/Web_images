from sqlalchemy import Table, MetaData, Column, Integer, String
from scr.authen.models import user

metadata = MetaData()

image = Table(
    'image',
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("file_name", String, unique=True, nullable=False),
    Column("url", String, unique=True, nullable=False),
    Column('attributes', String),
    # Column('edited_by', ForeignKey(user.c.id)),
)
