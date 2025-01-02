from flask import current_app
from datetime import datetime
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from models import Movie
from database import db
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def process_csv_file(file):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file)
        
        # Set default date for missing or invalid release dates
        DEFAULT_DATE = datetime(1900, 1, 1).date()
        df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce').dt.date
        df['release_date'] = df['release_date'].fillna(DEFAULT_DATE)
        
        # Handle required fields
        df['budget'] = pd.to_numeric(df['budget'], errors='coerce').fillna(0)
        df['original_language'] = df['original_language'].fillna('unknown')
        df['original_title'] = df['original_title'].fillna('Untitled')
        df['title'] = df['title'].fillna('Untitled')
        df['production_company_id'] = pd.to_numeric(df['production_company_id'], errors='coerce').fillna(1)
        df['genre_id'] = pd.to_numeric(df['genre_id'], errors='coerce').fillna(1)
        
        # Handle nullable fields
        df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce').fillna(0)
        df['runtime'] = pd.to_numeric(df['runtime'], errors='coerce').fillna(0)
        df['vote_average'] = pd.to_numeric(df['vote_average'], errors='coerce').fillna(0)
        df['vote_count'] = pd.to_numeric(df['vote_count'], errors='coerce').fillna(0)
        
        # Handle languages array and strip unnecessary characters
        df['languages'] = df['languages'].apply(lambda x: 
            [] if pd.isna(x) or x in ('[]', '[,]', '{}') else 
            [lang.strip().lower() for lang in x.strip('{}[]').split(',') if lang.strip()]
        )

        # Process records in batches for more efficient bulk insertions
        chunk_size = 1000
        total_rows = len(df)
        
        for start_idx in range(0, total_rows, chunk_size):
            end_idx = min(start_idx + chunk_size, total_rows)
            chunk = df.iloc[start_idx:end_idx]
            
            # Prepare the movies data for batch insertion
            movies_data = []
            for _, row in chunk.iterrows():
                movie_data = {
                    'budget': row['budget'],
                    'homepage': row['homepage'] if pd.notna(row['homepage']) else None,
                    'original_language': row['original_language'],
                    'original_title': row['original_title'],
                    'overview': row['overview'],
                    'release_date': row['release_date'],
                    'revenue': row['revenue'],
                    'runtime': row['runtime'],
                    'status': row['status'],
                    'title': row['title'],
                    'vote_average': row['vote_average'],
                    'vote_count': row['vote_count'],
                    'production_company_id': row['production_company_id'],
                    'genre_id': row['genre_id'],
                    'languages': row['languages'] if row['languages'] else []
                }
                movies_data.append(movie_data)
            
            # Insert data in bulk
            db.session.bulk_insert_mappings(Movie, movies_data)
            db.session.flush()
        
        db.session.commit()
        return True, f"Successfully processed {total_rows} movies."

    except SQLAlchemyError as e:
        db.session.rollback()
        return False, f"Database error: {str(e)}"
    except Exception as e:
        # Handling general exception errors and cause if any
        if hasattr(e, '__cause__') and e.__cause__ is not None:
            return False, f"Error: {str(e.__cause__)}"
        return False, f"Error: {str(e)}"
