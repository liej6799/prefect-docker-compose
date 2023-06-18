from prefect import flow, task
from postgres import TargetPostgres, PiHoleRawPostgres, PiHoleDomainPostgres
import os
import pandas as pd
import numpy as np
import asyncio
@task
def initiate_connection():
    return PiHoleRawPostgres(conn=TargetPostgres()), PiHoleDomainPostgres(conn=TargetPostgres())

@task 
def raw_extract():
    import requests
    url = os.environ['PIHOLE_API_URL']
    auth = os.environ['PIHOLE_API_AUTH']
    querystring = {"auth":auth,"getAllQueries":""}
    response = requests.request("POST", url, params=querystring)
    return pd.DataFrame(response.json()['data'])

@task 
async def process_extract(conn):
    return pd.DataFrame(await conn.read(), columns=['id', 'domain'])


@task
def raw_transform(data):
    # step 1 drop unused column
    data = data[[0, 1, 2, 3, 4, 6, 7]]
    data[4] = np.where(data[4]=='1', '8.8.8.8#53', '8.8.4.4#53')
    return data

@task 
async def process_transform_load(data, conn):
    import requests
    from requests.adapters import HTTPAdapter
    import pandas

    for i in data.iterrows():

        for protocol in ['http://', 'https://']:
            try:
                # try get
                res = requests.get(protocol + i[1]['domain'])
                data = {
                    "ph_domain_id": i[1]['id'],
                    "method": 'GET',
                    "response": res.text,
                    "status": res.status_code
                }
                print(data)
               
                
            except Exception as a:

                print(a)
        
    # requests.get(data)
    # print(data)
    # step 1 drop unused column
    # data = data[[0, 1, 2, 3, 4, 6, 7]]
    # data[4] = np.where(data[4]=='1', '8.8.8.8#53', '8.8.4.4#53')
    # return data



@task
async def raw_load(data, conn):
    for i in conn:
        await i.write(data)

@flow(name="PiHole Raw Data Flow")
async def raw_flow():
    raw, domain = initiate_connection()
    extract_res = raw_extract()
    data = raw_transform(extract_res)
    await raw_load(data, [raw, domain])

@flow(name="PiHole Process Data Flow")
async def process_flow():
    raw, domain = initiate_connection()
    extract_res = await process_extract(domain)
    await process_transform_load(extract_res, domain)




if __name__ == "__main__":
    #asyncio.run(raw_flow())
    asyncio.run(process_flow())
    

