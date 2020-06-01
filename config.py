import os


class development():
    dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"
    SQLALCHEMY_DATABASE_URI = dbdir
