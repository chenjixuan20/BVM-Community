from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# 配置app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:00000000@localhost:3306/dou_ban_3?charset=utf8mb4"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["SQLALCHEMY_ECHO"] = False
db = SQLAlchemy(app)

# user和tag和双向连接表，多对多关系
user_like_tags = db.Table('UserLikeTags', db.metadata,
                          db.Column('t_id', db.Integer, db.ForeignKey('tag.t_id'), primary_key=True),
                          db.Column('u_id', db.Integer, db.ForeignKey('user.u_id'), primary_key=True),
                          )

# book和tag的双向连接表，多对多关系
tag_associate_book = db.Table('TagToBook', db.metadata,
                              db.Column('t_id', db.Integer, db.ForeignKey('tag.t_id'), primary_key=True),
                              db.Column('b_id', db.Integer, db.ForeignKey('book.b_id'), primary_key=True),
                              )

# movie和tag的双向连接表，多对多关系
tag_associate_movie = db.Table('TagToMovie', db.metadata,
                               db.Column('t_id', db.Integer, db.ForeignKey('tag.t_id'), primary_key=True),
                               db.Column('mo_id', db.Integer, db.ForeignKey('movie.mo_id'), primary_key=True),
                               )

# music和tag的双向连接表，多对多关系
tag_associate_music = db.Table('TagToMusic', db.metadata,
                               db.Column('t_id', db.Integer, db.ForeignKey('tag.t_id'), primary_key=True),
                               db.Column('mu_id', db.Integer, db.ForeignKey('music.mu_id'), primary_key=True)
                               )


## 推荐算法使用到的数据库
# 推荐用户user电影movie,多对多关系
recommend_user_movie = db.Table('RecommendMovie', db.metadata,
                                db.Column('u_id', db.Integer, db.ForeignKey('user.u_id'), primary_key=True),
                                db.Column('mo_id', db.Integer, db.ForeignKey('movie.mo_id'), primary_key=True)
                                )
# 推荐用户user音乐music,多对多关系
recommend_user_music = db.Table('RecommendMusic', db.metadata,
                                db.Column('u_id', db.Integer, db.ForeignKey('user.u_id'), primary_key=True),
                                db.Column('mu_id', db.Integer, db.ForeignKey('music.mu_id'), primary_key=True)
                                )
# 推荐用户user书籍book,多对多关系
recommend_user_book = db.Table('RecommendBook', db.metadata,
                               db.Column('u_id', db.Integer, db.ForeignKey('user.u_id'), primary_key=True),
                               db.Column('b_id', db.Integer, db.ForeignKey('book.b_id'), primary_key=True)
                               )


# 用户点击电影的次数
class UserClickMovie(db.Model):
    __tablename__ = 'UserClickMoive'
    u_id = db.Column(db.Integer, primary_key=True)
    mo_id = db.Column(db.Integer, primary_key=True)
    times = db.Column(db.Integer, default=0)


# 用户点击音乐的次数
class UserClickMusic(db.Model):
    __tablename__ = 'UserClickMusic'
    u_id = db.Column(db.Integer, primary_key=True)
    mu_id = db.Column(db.Integer, primary_key=True)
    times = db.Column(db.Integer, default=0)


# 用户点击书籍的次数
class UserClickBook(db.Model):
    __tablename__ = 'UserClickBook'
    u_id = db.Column(db.Integer, primary_key=True)
    b_id = db.Column(db.Integer, primary_key=True)
    times = db.Column(db.Integer, default=0)


# 用户表
class User(db.Model):
    __tablename__ = 'user'
    u_id = db.Column(db.Integer, primary_key=True)
    u_openid = db.Column(db.String(255))
    u_session = db.Column(db.String(255))
    u_gender = db.Column(db.Boolean)
    u_picture = db.Column(db.String(255))
    u_age = db.Column(db.Integer)
    u_name = db.Column(db.String(50))
    moviecomments = db.relationship('Commentmovie', back_populates='user')
    musiccomments = db.relationship('Commentmusic', back_populates='user')
    bookcomments = db.relationship('Commentbook', back_populates='user')
    moviemarks = db.relationship('Markmovie', back_populates='user')
    musicmarks = db.relationship('Markmusic', back_populates='user')
    bookmarks = db.relationship('Markbook', back_populates='user')
    recommendmovies = db.relationship('Movie', secondary=recommend_user_movie, backref=db.backref('recommendtousers'))
    recommendmusic = db.relationship('Music', secondary=recommend_user_music, backref=db.backref('recommendtousers'))
    recommendbook = db.relationship('Book', secondary=recommend_user_book, backref=db.backref('recommendtousers'))

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

# 电影评论表，一对多关系
class Commentmovie(db.Model):
    __tablename__ = 'commentmovie'
    # com_id = db.Column(db.Integer,primary_key=True)
    com_user = db.Column(db.Integer, db.ForeignKey('user.u_id'), primary_key=True, autoincrement=False)
    com_movie = db.Column(db.Integer, db.ForeignKey('movie.mo_id'), primary_key=True, autoincrement=False)
    comment = db.Column(db.String(1000))
    date = db.Column(db.DATETIME, nullable=False, server_default=text('NOW()'))
    score = db.Column(db.Float)
    user = db.relationship('User', back_populates='moviecomments')
    movie = db.relationship('Movie', back_populates='comments')

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict
    __mapper_args__ = {
        "order_by":date.desc()
    }


# 音乐评论表，一对多关系
class Commentmusic(db.Model):
    __tablename__ = 'commentmusic'
    # com_id = db.Column(db.Integer,primary_key=True)
    com_user = db.Column(db.Integer, db.ForeignKey('user.u_id'), primary_key=True, autoincrement=False)
    com_music = db.Column(db.Integer, db.ForeignKey('music.mu_id'), primary_key=True, autoincrement=False)
    comment = db.Column(db.String(1000))
    date = db.Column(db.DATETIME, nullable=False, server_default=text('NOW()'))
    score = db.Column(db.Float)
    user = db.relationship('User', back_populates='musiccomments')
    music = db.relationship('Music', back_populates='comments')

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict
    __mapper_args__ = {
        "order_by":date.desc()
    }

# 书籍评论表，一对多关系
class Commentbook(db.Model):
    __tablename__ = 'commentbook'
    # com_id = db.Column(db.Integer,primary_key=True)
    com_user = db.Column(db.Integer, db.ForeignKey('user.u_id'), primary_key=True, autoincrement=False)
    com_book = db.Column(db.Integer, db.ForeignKey('book.b_id'), primary_key=True, autoincrement=False)
    comment = db.Column(db.String(1000))
    date = db.Column(db.DATETIME, nullable=False, server_default=text('NOW()'))
    score = db.Column(db.Float)
    user = db.relationship('User', back_populates='bookcomments')
    book = db.relationship('Book', back_populates='comments')

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

    __mapper_args__ = {
        "order_by":date.desc()
    }
# 电影标记表，一对多关系
class Markmovie(db.Model):
    __tablename__ = 'markmovie'
    mark_user = db.Column(db.Integer, db.ForeignKey('user.u_id'), primary_key=True, autoincrement=False)
    mark_movie = db.Column(db.Integer, db.ForeignKey('movie.mo_id'), primary_key=True, autoincrement=False)
    want_date = db.Column(db.DATETIME)
    seen_date = db.Column(db.DATETIME)
    user = db.relationship('User', back_populates='moviemarks')
    movie = db.relationship('Movie', back_populates='marks')
    __mapper_args__ = {
        "order_by":seen_date.desc()
    }

# 音乐标记表，一对多关系
class Markmusic(db.Model):
    __tablename__ = 'markmusic'
    mark_user = db.Column(db.Integer, db.ForeignKey('user.u_id'), primary_key=True, autoincrement=False)
    mark_music = db.Column(db.Integer, db.ForeignKey('music.mu_id'), primary_key=True, autoincrement=False)
    want_date = db.Column(db.DATETIME)
    seen_date = db.Column(db.DATETIME)
    user = db.relationship('User', back_populates='musicmarks')
    music = db.relationship('Music', back_populates='marks')

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict
    __mapper_args__ = {
        "order_by":seen_date.desc()
    }



# 书籍标记表，一对多关系
class Markbook(db.Model):
    __tablename__ = 'markbook'
    mark_user = db.Column(db.Integer, db.ForeignKey('user.u_id'), primary_key=True, autoincrement=False)
    mark_book = db.Column(db.Integer, db.ForeignKey('book.b_id'), primary_key=True, autoincrement=False)
    want_date = db.Column(db.DATETIME)
    seen_date = db.Column(db.DATETIME)
    user = db.relationship('User', back_populates='bookmarks')
    book = db.relationship('Book', back_populates='marks')

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict
    __mapper_args__ = {
        "order_by":seen_date.desc()
    }



# 电影表
class Movie(db.Model):
    __tablename__ = 'movie'
    mo_id = db.Column(db.Integer, primary_key=True)
    mo_English_name = db.Column(db.String(225), nullable=True, index=True)
    mo_name = db.Column(db.String(255), nullable=True, index=True)
    mo_introduction = db.Column(db.String(1000), nullable=True)
    mo_nation = db.Column(db.String(40), nullable=True)
    mo_heat = db.Column(db.Integer(), nullable=True)
    mo_picture = db.Column(db.String(5000), nullable=True)
    mo_length = db.Column(db.String(100), nullable=True)
    mo_score = db.Column(db.Integer, nullable=True)
    mo_date = db.Column(db.String(20), nullable=True)
    comments = db.relationship('Commentmovie', back_populates='movie')
    marks = db.relationship('Markmovie', back_populates='movie')

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

    def getMyName(self):
        return "Movie"


# 音乐表
class Music(db.Model):
    __tablename__ = 'music'
    mu_id = db.Column(db.Integer, primary_key=True)
    mu_name = db.Column(db.String(255), nullable=True, index=True)
    mu_introduction = db.Column(db.String(1000), nullable=True)
    mu_singer = db.Column(db.String(100), nullable=True)
    mu_heat = db.Column(db.Integer, nullable=True)
    mu_picture = db.Column(db.String(5000), nullable=True)
    mu_score = db.Column(db.Integer, nullable=True)
    mu_date = db.Column(db.String(20), nullable=True)
    comments = db.relationship('Commentmusic', back_populates='music')
    marks = db.relationship('Markmusic', back_populates='music')

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

    def getMyName(self):
        return "Music"


# 书籍表
class Book(db.Model):
    __tablename__ = 'book'
    b_id = db.Column(db.Integer, primary_key=True)
    b_name = db.Column(db.String(255), nullable=True, index=True)
    b_introduction = db.Column(db.String(1000), nullable=True)
    b_pulishing_house = db.Column(db.String(500), nullable=True)
    b_picture = db.Column(db.String(500))
    b_writer = db.Column(db.String(100), nullable=True)
    b_writer_intro = db.Column(db.String(1000), nullable=True)
    b_score = db.Column(db.Integer, nullable=True)
    b_heat = db.Column(db.Integer, nullable=True)
    b_date = db.Column(db.String(20), nullable=True)
    comments = db.relationship('Commentbook', back_populates='book')
    marks = db.relationship('Markbook', back_populates='book')

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

    def getMyName(self):
        return "Book"


# 标签表
class Tag(db.Model):
    __tablename__ = 'tag'
    t_id = db.Column(db.Integer, primary_key=True)
    t_tag = db.Column(db.String(100), nullable=False)
    movies = db.relationship('Movie', secondary=tag_associate_movie, backref=db.backref('TagstoMovie'))
    books = db.relationship('Book', secondary=tag_associate_book, backref=db.backref('TagstoBook'))
    music = db.relationship('Music', secondary=tag_associate_music, backref=db.backref('TagstoMusic'))
    users = db.relationship('User', secondary=user_like_tags, backref=db.backref('UserlikeTags'))

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

    def getMyName(self):
        return "Tag"


# 定义manager
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
