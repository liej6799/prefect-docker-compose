
from prefect import flow, task
from postgres import TargetPostgres, PiHoleRawPostgres, PiHoleDomainPostgres
from sqlite import SourceSQLite, QueriesSQLite
import os
import pandas as pd
import numpy as np
import asyncio

@task
def initiate_connection():
    return QueriesSQLite(conn=SourceSQLite()), PiHoleRawPostgres(conn=TargetPostgres()), PiHoleDomainPostgres(conn=TargetPostgres())

@task
async def extract(conn):
    response = await conn.read()
    return pd.DataFrame(response)
@task
def transform(data):
    # step 1 drop unused column
    return data

@task
async def load(data, conn):
    for i in conn:
        await i.write(data)

@flow(name="PiHole Raw Data Flow")
async def flow():
    source, raw, domain = initiate_connection()
    extract_res = await extract(source)
    data = transform(extract_res)
    await load(data, [raw, domain])


if __name__ == "__main__":
    asyncio.run(flow())
    #asyncio.run(RawDataFlow().flow())
    # asyncio.run(process_flow())
    

