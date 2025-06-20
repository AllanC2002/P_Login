# database Accounts
from dotenv import load_dotenv
import os
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

def conection_accounts():
    host = os.getenv("DBA_HOSTIP")
    port = os.getenv("DBA_PORT")
    user = os.getenv("DBA_USER")
    password = urllib.parse.quote_plus(os.getenv("DBA_PASSWORD"))  # Escapa símbolos
    dbname = os.getenv("DBA_NAME")

    connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}"
    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    return Session()


