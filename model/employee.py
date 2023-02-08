from sqlalchemy.orm import relationship

from model import Base


class Employee(Base):
    __tablename__ = 'employee'
