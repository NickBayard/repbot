from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.org import sessionmaker
from lib.base import Base


_engine = None
_Session = None


def create_db_session(db_file=None):
    global _Session
    global _engine

    if _engine is None:
        if db_file is None:
            raise Exception('db_file must be specified to create Session object.')

        path = Path(db_file)
        engine_path = 'sqlite://{}{}'
        if 'memory' in db_file.lower():
            absolute = ''
            db_path = ''
        else:
            absolute = '/' if path.is_absolute() else ''
            db_path = str(path)
        _engine = create_engine(engine_path.format(absolute, db_path))
        Base.metadata.create_all(_engine)

    if _Session is None:
        _Session = sessionmaker(bind=_engine)

    return _Session()
