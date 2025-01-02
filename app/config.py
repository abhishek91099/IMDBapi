from urllib.parse import quote_plus

password = 'root@123'
encoded_password = quote_plus(password)

config = {
    'SQLALCHEMY_DATABASE_URI': f'postgresql://postgres:{encoded_password}@127.0.0.1:5432/resumeproject',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'MAX_CONTENT_LENGTH': 100 * 1024 * 1024,  # 100MB max file size
    'ALLOWED_EXTENSIONS': {'csv'}
}
