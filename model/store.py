from sqlalchemy.orm import relationship

from model import Base


class Store(Base):
    __tablename__ = 'store'
