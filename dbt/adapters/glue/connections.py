from contextlib import contextmanager
import agate
from typing import Any, List, Dict,Optional
from dbt.adapters.sql import SQLConnectionManager
from dbt.contracts.connection import AdapterResponse
from dbt.exceptions import (
    FailedToConnectError,
    DbtRuntimeError
)
import dbt
from dbt.adapters.glue.gluedbapi import GlueConnection, GlueCursor
from dbt.events import AdapterLogger

logger = AdapterLogger("Glue")


class GlueSessionState:
    OPEN = "open"
    FAIL = "fail"

class ReturnCode:
    OK = "OK"

class GlueConnectionManager(SQLConnectionManager):
    TYPE = "glue"
    GLUE_CONNECTIONS_BY_THREAD: Dict[str, GlueConnection] = {}


    @classmethod
    def open(cls, connection):
        if connection.state == "open":
            logger.debug("Connection is already open, skipping open.")
            return connection

        credentials = connection.credentials
        try:
            key = cls.get_thread_identifier()
            if not cls.GLUE_CONNECTIONS_BY_THREAD.get(key):
                logger.debug(f"opening a new glue connection for thread : {key}")
                cls.GLUE_CONNECTIONS_BY_THREAD[key]: GlueConnection = GlueConnection(credentials=credentials)
                cls.GLUE_CONNECTIONS_BY_THREAD[key].connect()
            connection.state = GlueSessionState.OPEN
            connection.handle = cls.GLUE_CONNECTIONS_BY_THREAD[key]
            return connection
        except Exception as e:
            logger.error(
                f"Got an error when attempting to open a GlueSession : {e}"
            )
            connection.handle = None
            connection.state = GlueSessionState.FAIL
            raise FailedToConnectError(f"Got an error when attempting to open a GlueSessions: {e}")

    def cancel(self, connection):
        """ cancel ongoing queries """
        connection.handle.cancel()

    @contextmanager
    def exception_handler(self, sql: str):
        try:
            yield
        except Exception as e:
            logger.debug("Unhandled error while running:\n{}".format(sql))
            self.release()
            if isinstance(e, DbtRuntimeError):
                # during a sql query, an internal to dbt exception was raised.
                # this sounds a lot like a signal handler and probably has
                # useful information, so raise it without modification.
                raise
            raise DbtRuntimeError(str(e))

    @classmethod
    def get_response(cls, cursor) -> AdapterResponse:
        """
        new to support dbt 0.19: this method replaces get_response
        """
        message = ReturnCode.OK
        return AdapterResponse(
            _message=message,
        )

    @classmethod
    def get_result_from_cursor(cls, cursor: GlueCursor, limit:Optional[int]) -> agate.Table:
        data: List[Any] = []
        column_names: List[str] = []
        if cursor.description is not None:
            column_names = [col[0] for col in cursor.description()]
            if limit:
                rows = cursor.fetchmany(limit)
            else:
                rows = cursor.fetchall()
            data = cls.process_results(column_names, rows)
        return dbt.clients.agate_helper.table_from_data_flat(
            data,
            column_names
        )

    # No transactions on Spark....
    def add_begin_query(self, *args, **kwargs):
        logger.debug("NotImplemented: add_begin_query")

    def add_commit_query(self, *args, **kwargs):
        logger.debug("NotImplemented: add_commit_query")

    def commit(self, *args, **kwargs):
        logger.debug("NotImplemented: commit")

    def rollback(self, *args, **kwargs):
        logger.debug("NotImplemented: rollback")

    def cleanup_all(self):
        logger.debug("cleanup called")
        for connection in self.GLUE_CONNECTIONS_BY_THREAD.values():
            try:
                connection.close_session()
            except Exception as e:
                logger.exception(f"failed to close session : {e}")
                logger.debug("connection not yet initialized")