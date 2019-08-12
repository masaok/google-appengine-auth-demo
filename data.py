from google.appengine.ext import ndb

class Teacher(ndb.Model):
    name = ndb.StringProperty(required=True)
    # email = ndb.StringProperty(required=True)

class Course(ndb.Model):
    name = ndb.StringProperty(required=True)
    teachers = ndb.KeyProperty(Teacher,repeated=True)

    @classmethod
    def query_courses(cls, ancestor_key):
      return cls.query(ancestor=ancestor_key).order(cls.name)

class User(ndb.Model):
    name = ndb.StringProperty(required=True)
    username = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)

class Post(ndb.Model):
    author = ndb.KeyProperty(User, required=True)
    board = ndb.StringProperty(required=True)
    content = ndb.StringProperty(required=True)
    time = ndb.DateTimeProperty(auto_now_add=True)

class Enrollment(ndb.Model):
    user = ndb.KeyProperty(User)
    course = ndb.KeyProperty(Course)
