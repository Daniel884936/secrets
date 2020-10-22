from sql.database import SessionLocal

#Secret key for token
SECRET_KEY = 'EDANIELTEJADA809'

# Dependency 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()
        