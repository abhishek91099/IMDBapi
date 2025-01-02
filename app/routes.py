from flask import Blueprint, request, jsonify
from models import Movie
from utils import allowed_file, process_csv_file
from database import db

bp = Blueprint('movies', __name__)

@bp.route('/upload', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    print(request.files)
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file'}), 400
    
    success, message = process_csv_file(file)
    if success:
        return jsonify({'message': message}), 200
    print(message)
    return jsonify({'error': message}), 500

@bp.route('/listmovies', methods=['GET'])
def get_movies():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    year = request.args.get('year', type=int)
    language = request.args.get('languages')
    sort_by = request.args.get('sort_by', 'release_date')
    sort_order = request.args.get('sort_order', 'asc')

    
    query = Movie.query
    
    if year:
        query = query.filter(db.extract('year', Movie.release_date) == year)
    if language:
        query = query.filter(Movie.languages.contains([language.lower()]))
    
    if sort_by == 'release_date':
        query = query.order_by(Movie.release_date.asc() if sort_order == 'asc' else Movie.release_date.desc())
    elif sort_by == 'rating':
        query = query.order_by(Movie.vote_average.asc() if sort_order == 'asc' else Movie.vote_average.desc())
    
    pagination = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'movies': [movie.to_dict() for movie in pagination.items]
    })