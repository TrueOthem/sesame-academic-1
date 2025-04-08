import contextlib
from datetime import datetime
import sys

from sqlalchemy import create_engine, event, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


class DB():

    def __init__(self):
        self.engine = None
        self.metadata = MetaData()
        self.Base = declarative_base(metadata=self.metadata)
        self.test_session = None

        @event.listens_for(self.Base, 'before_insert', propagate=True)
        def before_insert(mapper, connection, target):
            if hasattr(target, 'created_at'):
                target.created_at = datetime.utcnow()
            if hasattr(target, 'updated_at'):
                target.updated_at = datetime.utcnow()

        @event.listens_for(self.Base, 'before_update', propagate=True)
        def before_update(mapper, connection, target):
            if hasattr(target, 'updated_at'):
                target.updated_at = datetime.utcnow()

    def test_mode_enable(self):
        self.test_session = self.connection()

    def test_mode_disable(self):
        self.test_session.rollback()
        self.test_session.close()
        self.test_session = None

    def connect(self, url):
        import os
        if os.environ.get('SKIP_DB_CONNECTION') == 'true':
            print('Skipping database connection')
            return
        if not self.engine:
            # Updated parameters for SQLAlchemy 2.0 compatibility
            self.engine = create_engine(
                url,
                pool_size=5,
                max_overflow=0,
                pool_recycle=3600,
                pool_pre_ping=True,  # Check connection validity before using it
                future=True  # Use SQLAlchemy 2.0 behavior
            )

    def connection(self):
        import os
        if os.environ.get('SKIP_DB_CONNECTION') == 'true':
            print('Skipping database connection in connection method')
            return None
        if self.test_session is None:
            # get new connection from the pool
            if not self.engine:
                print('No database engine available')
                return None
            # Updated for SQLAlchemy 2.0 compatibility
            session_factory = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine,
                expire_on_commit=False,
                future=True  # Use SQLAlchemy 2.0 behavior
            )
            return scoped_session(session_factory)
        else:
            # nested transaction that we'll roll back
            self.test_session.begin_nested()
            return self.test_session

    @contextlib.contextmanager
    def session(self):
        session = self.connection()

        import os
        if os.environ.get('SKIP_DB_CONNECTION') == 'true' or session is None:
            print('Skipping database session')
            yield None
            return

        # convenience for querying through models
        self.Base.query = session.query_property()

        try:
            yield session
        except:
            session.rollback()
            raise
        finally:
            if self.test_session is None:
                # return connection to pool
                session.close()

            self.Base.query = None

    def save(self, instance):
        with self.session() as session:
            if session is None:
                print('Skipping database save')
                return
            session.add(instance)
            session.commit()


sys.modules[__name__] = DB()
