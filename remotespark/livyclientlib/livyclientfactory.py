# Copyright (c) 2015  aggftw@gmail.com
# Distributed under the terms of the Modified BSD License.
from .log import Log
from .connectionstringutil import get_connection_string_elements
from .livysession import LivySession
from .livyclient import LivyClient
from .reliablehttpclient import ReliableHttpClient
from .constants import Constants


class LivyClientFactory(object):
    """Spark client for Livy endpoint"""
    logger = Log()

    def __init__(self):
        pass

    def build_client(self, connection_string):
        cso = get_connection_string_elements(connection_string)

        headers = self._get_headers()

        http_client = ReliableHttpClient(cso.url, headers, cso.username, cso.password)

        spark_session = self._create_session(http_client, Constants.session_kind_spark)
        pyspark_session = self._create_session(http_client, Constants.session_kind_pyspark)

        return LivyClient(spark_session, pyspark_session)

    def _create_session(self, http_client, kind):
        session = LivySession(http_client, kind)
        session.start()
        return session

    def _get_headers(self):
        return {"Content-Type": "application/json"}
