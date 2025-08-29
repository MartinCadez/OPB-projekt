from typing import Any, Dict, List, Optional
import pandas as pd
from sqlalchemy import create_engine, Table, Column, MetaData, insert, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError


class PostgresDB:
    def __init__(self, user: str, password: str, host: str, port: int, database: str):
        self.connection_url = (
            f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
        )
        self.engine: Engine = create_engine(self.connection_url)
        self.metadata = MetaData()

    def run_query(
        self, query: str, params: Optional[Dict[str, Any]] = None
    ) -> pd.DataFrame:
        try:
            with self.engine.connect() as conn:
                df = pd.read_sql(text(query), conn, params=params)
            return df
        except SQLAlchemyError as e:
            raise RuntimeError(f"Query failed: {e}")

    def execute(self, query: str, params: Optional[Dict[str, Any]] = None) -> None:
        try:
            with self.engine.begin() as conn:
                conn.execute(text(query), params or {})
        except SQLAlchemyError as e:
            raise RuntimeError(f"Execution failed: {e}")

    def insert_dataframe(
        self, df: pd.DataFrame, table_name: str, if_exists: str = "append"
    ) -> None:
        try:
            df.to_sql(table_name, self.engine, if_exists=if_exists, index=False)
        except SQLAlchemyError as e:
            raise RuntimeError(f"Insert DataFrame failed: {e}")

    def insert_dict(self, table_name: str, data: Dict[str, Any]) -> None:
        try:
            table = Table(table_name, self.metadata, autoload_with=self.engine)
            stmt = insert(table).values(**data)
            with self.engine.begin() as conn:
                conn.execute(stmt)
        except SQLAlchemyError as e:
            raise RuntimeError(f"Insert dict failed: {e}")

    def create_table(self, table_name: str, columns: List[Column]) -> None:
        try:
            table = Table(table_name, self.metadata, *columns)
            self.metadata.create_all(self.engine, tables=[table])
        except SQLAlchemyError as e:
            raise RuntimeError(f"Create table failed: {e}")

    def list_tables(self) -> List[str]:
        self.metadata.reflect(bind=self.engine)
        return list(self.metadata.tables.keys())
