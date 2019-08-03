import os

SQLALCHEMY_DATABASE_URI='mysql://root:westos@localhost/movieProject'
SQLALCHEMY_TRACK_MODIFICATIONS=True
SECRET_KEY='westos'

PER_PAGE=5

BASE_DIR=os.path.dirname(__file__)
FC_DIR=os.path.join(BASE_DIR,'app/static/userImg/faceImg')

MOVIE_DIR=os.path.join(BASE_DIR,'app/static/adminImg/movie')