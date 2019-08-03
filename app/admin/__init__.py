from flask import Blueprint

admin=Blueprint('admin',__name__)


from app.admin.views.main import *
from app.admin.views.tags import *

from app.admin.views.movies import *

