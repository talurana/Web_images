from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey
from scr.authen.models import user

metadata = MetaData()

image = Table(
    'image',
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("file_name", String, unique=True, nullable=False),
    Column("url", String, unique=True, nullable=False),
    Column('attributes', String),
    #Column('edited_by', ForeignKey(user.c.id, name="fk_image_user_id")),
    Column('edited_by_email', ForeignKey(user.c.email, name="fk_image_user_email")),
)
