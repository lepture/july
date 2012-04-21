from july.database import db
from sqlalchemy import Column, Integer, String, Text


class Post(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    content = Column(Text)
