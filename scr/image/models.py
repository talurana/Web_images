from sqlalchemy import Column, Integer, String, ForeignKey #, Table, BigInteger

from scr.db import Base

# можно в будущем сделать через Many2Many, но сервис будет максимум 0.5rps, потому не хочется тратить на это 1000 лет

# attribute2image = Table('attribute2image', Base.metadata,
#     Column('id', BigInteger, primary_key=True),
#     Column('image_id', BigInteger, ForeignKey('image.id')),
#     Column('attribute_id', BigInteger, ForeignKey('attribute.id'))
# )


# class Attribute(Base):
#     __tablename__ = "attribute"
#     id = Column(Integer, primary_key=True, unique=True)
#     attribute_name = Column(String, unique=True, nullable=False)
#
#     images = relationship('Person', secondary="attribute2image", back_populates='images')
#

class Image(Base):
    __tablename__ = "image"
    id = Column(Integer, primary_key=True, unique=True)
    image_name = Column(String, unique=True, nullable=False)
    attributes = Column(String)
    url = Column(String, unique=True, nullable=False)
    last_change = Column(ForeignKey('user.email'))

    # attributes = relationship('Playlist', secondary="attribute2image", back_populates='attributes')
