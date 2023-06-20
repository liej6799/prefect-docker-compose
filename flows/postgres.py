
import asyncpg
from typing import Tuple


class CredsPostgres():
    def __init__(self):
        pass


class TargetPostgres(CredsPostgres):
    host = 'database'
    user = 'postgres'
    pw = 'postgres'
    db = 'prefect'
    port = 5432

class Postgres():
    def __init__(self, conn: CredsPostgres):
        self.table = self.default_table

        self.host = conn.host
        self.user = conn.user
        self.pw = conn.pw
        self.db = conn.db
        self.port = conn.port

    async def _connect(self):
        self.conn = await asyncpg.connect(user=self.user, password=self.pw, database=self.db, host=self.host, port=self.port)

    async def read(self):
        await self._connect()
        statement = self._read()
        return await self.conn.fetch(statement)

    async def write(self, data):
        await self._connect()
        args_str = ','.join([self._write(u)
                            for u in data.iterrows()])

        async with self.conn.transaction():
            try:
                print('try insert')
                await self.conn.execute(f"INSERT INTO {self.table} VALUES {args_str} ON CONFLICT DO NOTHING")
            except Exception as a:
                print(a)
                # when restarting a subscription, some exchanges will re-publish a few messages
                pass


class PiHoleRawPostgres(Postgres):
    default_table = 'ph_raw'

    def _read(self):
        NotImplemented

    def _write(self, data):
        return f"(DEFAULT,'{data[1][0]}','{data[1][1]}','{data[1][2]}','{data[1][3]}','{data[1][4]}','{data[1][5]}','{data[1][6]}')"


class PiHoleDomainPostgres(Postgres):
    default_table = 'ph_domain'

    def _read(self):
        return f"SELECT id, domain FROM {self.table} where isprocessyn = false"

    def _write(self, data):
        return f"(DEFAULT,'{data[1][2]}', false)"

class PiHoleDomainResponsePostgres(Postgres):
    default_table = 'ph_domain_response'

    def _write(self, data):
        return f"(DEFAULT,'{data[1][2]}', false)"

