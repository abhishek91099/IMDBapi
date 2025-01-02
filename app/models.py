from datetime import datetime
from database import db
from sqlalchemy.dialects.postgresql import ARRAY
class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    budget = db.Column(db.BigInteger, nullable=False)
    homepage = db.Column(db.String(255))
    original_language = db.Column(db.String(10), nullable=False)
    original_title = db.Column(db.String(255), nullable=False)
    overview = db.Column(db.Text)
    release_date = db.Column(db.Date, nullable=True)
    revenue = db.Column(db.BigInteger)
    runtime = db.Column(db.Integer)
    status = db.Column(db.String(50))
    title = db.Column(db.String(255), nullable=False)
    vote_average = db.Column(db.Float)
    vote_count = db.Column(db.Integer)
    production_company_id = db.Column(db.Integer, nullable=False)
    genre_id = db.Column(db.Integer, nullable=False)
    languages = db.Column(ARRAY(db.String(50)))

    def __repr__(self):
        return f"<Movie {self.title}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'budget': self.budget,
            'homepage': self.homepage,
            'original_language': self.original_language,
            'original_title': self.original_title,
            'overview': self.overview,
            'release_date': self.release_date.isoformat() if self.release_date else None,
            'revenue': self.revenue,
            'runtime': self.runtime,
            'status': self.status,
            'title': self.title,
            'vote_average': self.vote_average,
            'vote_count': self.vote_count,
            'production_company_id': self.production_company_id,
            'genre_id': self.genre_id,
            'languages': self.languages
        }