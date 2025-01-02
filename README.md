# IMDb Content Upload and Review System

This is a Flask-based application that allows users to upload movie-related data via CSV files and provides APIs to view and filter the uploaded data.

## Features

- CSV file upload for movie data
- Paginated API for viewing movies
- Filtering by year and language
- Sorting by release date and ratings
- Postgres database for data storage
- File size limit of 100MB

## Setup Instructions

1. Clone the repository:
```bash
git clone 
cd app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Change the Config in config.py:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

## API Documentation

### Upload CSV
- **Endpoint**: `/movie/upload`
- **Method**: POST
- **Content-Type**: multipart/form-data
- **Parameter**: file (CSV file)
- **Response**: Success/Error message

### Get Movies
- **Endpoint**: `/movies/listmovies`
- **Method**: GET
- **Query Parameters**:
  - page (default: 1)
  - per_page (default: 10)
  - year (optional)
  - languages (optional)
  - sort_by (optional: 'release_date' or 'rating')
  - sort_order (optional: 'asc' or 'desc')
- **Response**: Paginated list of movies with metadata



## Testing
You can test the APIs using the following curl commands:

1. Upload CSV:
```bash
curl -X POST -F "file=@movies.csv" http://localhost:5000/movies/upload
```

2. Get Movies:
```bash
curl "http://localhost:5000/movies/listmovies?page=1&per_page=10&year=2023&language=English&sort_by=rating&sort_order=desc"
```
