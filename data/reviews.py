"""
Модуль с определением модели рецензий для работы с базой данных.
"""
import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Reviews(SqlAlchemyBase):
    """
    Модель рецензии на сочинение.
    
    Attributes:
        id (int): Уникальный идентификатор рецензии
        task (str): Текст задания для сочинения
        source_text (str): Исходный текст (если есть)
        text (str): Текст сочинения
        ai_review (str): Сгенерированная AI рецензия
        created_date (datetime): Дата создания рецензии
        user_id (int): Идентификатор пользователя-владельца
        user (relationship): Связь с моделью пользователя
    """
    __tablename__ = 'reviews'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    task = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    source_text = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="нет")
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    ai_review = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')
    
    def __repr__(self):
        """
        Строковое представление объекта рецензии
        
        Returns:
            str: Строковое представление рецензии
        """
        return f"<Review #{self.id} by user #{self.user_id}>"