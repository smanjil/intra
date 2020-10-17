# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

import aiohttp
import datetime
import os
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch.helpers import async_streaming_bulk
from elasticapm.contrib.starlette import ElasticAPM, make_apm_client


apm = make_apm_client(
    {"SERVICE_NAME": "fastapi-app", "SERVER_URL": "http://apm-server:8200"}
)
es = AsyncElasticsearch(os.environ["ELASTICSEARCH_HOSTS"])
app = FastAPI()
app.add_middleware(ElasticAPM, client=apm)


@app.on_event("shutdown")
async def app_shutdown():
    await es.close()


@app.post('/create')
async def create_user(user):
    if not (await es.indices.exists(index="users")):
        await es.indices.create(index="users")
        
    return await es.index(index="users", body=user)


@app.get("/doc/{id}")
async def get_doc(id):
    return await es.get(index="users", id=id)


@app.get("/search/{query}")
async def search(query):
    return await es.search(
        index="users", body={"query": {"multi_match": {"query": query}}}
    )
    
    
@app.put("/update/{val}")
async def update(val):
    # response = []
    # docs = await es.search(
    #     index="users", body={"query": {"multi_match": {"query": val}}}
    # )
    # now = datetime.datetime.utcnow()
    # for doc in docs["hits"]["hits"]:
    #     response.append(
    return await es.update(
        index="users", id="aDuEMXUBGkvWpA3aisMe", body=val
    )
        # )


@app.get("/delete")
async def delete():
    return await es.delete_by_query(index="users", body={"query": {"match_all": {}}})


@app.get("/delete/{id}")
async def delete_id(id):
    try:
        return await es.delete(index="users", id=id)
    except NotFoundError as e:
        return e.info, 404
