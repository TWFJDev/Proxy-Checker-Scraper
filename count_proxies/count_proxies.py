from sqlalchemy.orm import sessionmaker
import models
from contextlib import contextmanager

SessionLocal = sessionmaker(bind=models.engine)

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def count_proxies():
    with get_session() as session:
        count = session.query(models.Proxies).count()
        print(f'{count} proxies in the database!\n')