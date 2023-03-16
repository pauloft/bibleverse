from sqlmodel import SQLModel, create_engine, Session

# Create a SQLite engine
sqlite_url = "sqlite:///bible.db"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args, echo=True)


# function to create the database using the table
# models if it does not exist
def init_db():
    SQLModel.metadata.create_all(engine)


# get_session used in dependency injection
def get_session() -> Session:
    with Session(engine) as session:
        yield session
