import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

passwd=os.getenv('passwd')
host=os.getenv('host')
port=os.getenv('port')
database = os.getenv('database')
user=os.getenv('user')



logger=logging.getLogger(__name__)

# DB_URL=f"postgresql://postgres:mypassword@0.0.0.0:7000/postgres"
DB_URL=f'postgresql://{user}:{passwd}@{host}:{port}/{database}'

class BackendConnector:

    @classmethod
    def get_engine(cls):
        logger.info(f'Creating Engine')
        engine=create_engine(
            DB_URL,
            echo=False,
            pool_size=2,
            pool_pre_ping=True,
        )
        logger.info('Engine Created')
        return engine
    
    @classmethod
    def get_sessionmaker(cls) -> sessionmaker:

        engine=cls.get_engine()
        logger.info('Creating Session')
        session:sessionmaker=sessionmaker(bind=engine)
        logger.info('Session Created')
        return session
    
    @classmethod
    def get_session(cls):
        session_maker=cls.get_sessionmaker()
        session=session_maker()
        return session

if __name__=="__main__":
    eng=BackendConnector.get_engine()
    print(eng)
    print(type(eng))
