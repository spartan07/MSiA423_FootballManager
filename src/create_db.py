import logging.config
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
import sys
import os


logger = logging.getLogger(__name__)
Base = declarative_base()


class user_input(Base):
    """ Defines the data model for the table user_input"""
    __tablename__ = 'user_input'
    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    Reactions = Column(Integer, unique=False, nullable=False)
    Potential = Column(Integer, unique=False, nullable=False)
    Age = Column(Integer, unique=False, nullable=False)
    BallControl = Column(Integer, unique=False, nullable=False)
    StandingTackle = Column(Integer, unique=False, nullable=False)
    Composure = Column(Integer, unique = False, nullable = False)
    Dribbling = Column(Integer, unique=False, nullable=False)
    Positioning = Column(Integer, unique=False, nullable=False)
    Finishing = Column(Integer, unique=False, nullable=False)
    GKReflexes = Column(Integer, unique=False, nullable=False)
    Position = Column(String(10), unique=False, nullable=False)
    Predicted_Val = Column(Float, unique= False, nullable=False)


    def __repr__(self):
        player_repr = "<Player(id='%i', reactions='%d', potential='%d', age='%d', ballcontrol='%d'," \
                      " standingtackle='%d', composure='%d',dribbling='%d',"\
                " positioning ='%d', finishing ='%d',gkreflexes = '%d',position ='%s', predictedval = '%f')>"
        return player_repr % (self.id, self.Reactions, self.Potential, self.Age,
                              self.BallControl, self.StandingTackle, self.Composure,
                              self.Dribbling, self.Positioning, self.Finishing,
                              self.GKReflexes, self.Position, self.Predicted_Val)


def create_db_sql(args):
    """Creates a SQLITE database (based on configuration) with User inputs table.
    Returns: Optional user argument with sql engine
    """
    try:
        print(args.engine_string)
        engine = create_engine(args.engine_string)
        logger.info("Creating sqlite database")
        Base.metadata.create_all(engine)
        logger.info("Database created with tables")
    except Exception as e:
        logger.error(e)
        sys.exit(1)


def create_db_rds(args):
    """
    Creates a RDS database (based on configuration) with User inputs table.
    """
    rds_config = args.config
    conn_type = rds_config["type"]
    host = rds_config["host"]
    port = rds_config["port"]
    database = rds_config["dbname"]
    user = os.environ.get('MYSQL_USER')
    password = os.environ.get('MYSQL_PASSWORD')
    engine_string = "{}://{}:{}@{}:{}/{}". \
        format(conn_type, user, password, host, port, database)
    try:

        engine = create_engine(engine_string)
        logger.info("Creating RDS database")
        Base.metadata.create_all(engine)
        logger.info("Database created with tables")
    except Exception as e:
        logger.error(e)
        sys.exit(1)


