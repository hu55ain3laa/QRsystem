import logging

from sqlmodel import Session

from app.core.db import engine, init_db
from app.models import SQLModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    logger.info("Creating SQLite tables")
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        init_db(session)


def main() -> None:
    logger.info("Initializing service")
    init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
