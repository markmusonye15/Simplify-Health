from db.database import db
from dataclasses import dataclass
from typing import Optional


@dataclass
class UserType:
    id: Optional[int]
    username: str
    email: str
    password: str


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=True)

    def create(self: UserType):
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)
        print(f"{self.username} has been added successfully!!")
        return self

    def update(self: UserType):
        db.session.commit()
        db.session.refresh(self)
        print(f"{self.username} has been updated successfully!!")
        return self

    def delete(self: UserType):
        db.session.delete(self)
        db.session.commit()
        print(f"{self.username} has been deleted successfully!!")
        return True
