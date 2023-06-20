import aiosqlite

class CredsPostgres():
    def __init__(self):
        pass

class SourceSQLite(CredsPostgres):
    path = '/root/pihole/pihole-FTL.db'

class SQLite():
    def __init__(self, conn: CredsPostgres):
        self.table = self.default_table

        self.path = conn.path
   
    async def _connect(self):
        self.conn = await aiosqlite.connect(database=self.path)

    async def read(self):
        await self._connect()
        statement = self._read()
        cursor = await self.conn.execute(statement)
        return await cursor.fetchall()
    
    async def close(self):
        await self.conn.close()

class QueriesSQLite(SQLite):
    default_table = 'queries'

    def _read(self):
        return f"select timestamp, type, domain, client, forward, reply_type,reply_time as duration from {self.default_table}"


 