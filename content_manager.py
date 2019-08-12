from google.appengine.api import users
from google.appengine.ext import ndb
from data import Post, User
from datetime import datetime
# from calendarDisplay import filterEvents


logout_url = users.create_logout_url('/')
login_url = users.create_login_url('/')

def format_posts(posts):
    return [(User.query().filter(User.key == post.author).get().username,
            post.content, post.time) for post in posts]

def populate_feed(current_user, current_board):
    chat_fields = {
        "sign_out": logout_url,
        "username": current_user.username,
        "user_name": current_user.name,
        "post_count": len(Post.query().filter(Post.author == current_user.key).fetch()),
        "user_count": len(User.query().fetch()),
        "posts": format_posts(Post.query().filter(Post.board == current_board).order(-Post.time).fetch(limit=30)),
        "users": User.query().order(User.username).fetch(),
        "board": current_board,
    }
    return chat_fields
