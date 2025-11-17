class Config:
    SECRET_KEY = "secret123"  # any string works
    SQLALCHEMY_DATABASE_URI = "sqlite:///lab8.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False