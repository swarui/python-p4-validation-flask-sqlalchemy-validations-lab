from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.exc import IntegrityError


db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = "authors"
    # Add validations and constraints

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates("name")
    def validate_name(self, key, name):
        if len(name) == 0:
            raise ValueError("Name must have a value")
        author = Author.query.filter_by(name=name).first()
        if author:
            raise ValueError("Author name not unique")
        return name

    @validates("phone_number")
    def validate_phone_number(self, key, phone_number):
        if len(phone_number) != 10:
            raise ValueError("Phone_number should contain exactly 10 digits")
        else:
            return phone_number

    def __repr__(self):
        return f"Author(id={self.id}, name={self.name})"


class Post(db.Model):
    __tablename__ = "posts"
    # Add validations and constraints

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates("title")
    def validate_title(self, key, title):
        if not title and len(title.strip()) == 0:
            raise ValueError("Title is requered")

        if not self.__is_title_clickable(title):
            raise ValueError("Title does not contain clickable phrase")

        return title

    @validates("content")
    def validate_content(self, key, content):
        if not len(content) >= 250:
            raise ValueError("Post content is at least 250 characters long.")
        else:
            return content

    @validates("summary")
    def validate_summary(self, key, summary):
        if not len(summary) < 250:
            raise ValueError("Post summary is a maximum of 250 characters.")
        else:
            return summary

    @validates("category")
    def validate_category(self, key, category):
        if not category in ("Fiction", "Non-Fiction"):
            raise ValueError("Post category is either Fiction or Non-Fiction.")
        else:
            return category

    def __is_title_clickable(self, title):
        clickable_strings = ("Won't Believe", "Secret", "Top", "Guess")
        is_clickable = False
        for s in clickable_strings:
            if s in title:
                is_clickable = True
        return is_clickable

    def __repr__(self):
        return f"Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})"