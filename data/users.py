import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):

    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    reviews = orm.relationship("Reviews", back_populates='user')

    def set_password(self, password):
        """
        Устанавливает хэшированный пароль пользователя
        
        Args:
            password (str): Пароль в открытом виде
        """
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        """
        Проверяет совпадение пароля с хэшем
        
        Args:
            password (str): Пароль для проверки
            
        Returns:
            bool: True если пароль верный, иначе False
        """
        return check_password_hash(self.hashed_password, password)