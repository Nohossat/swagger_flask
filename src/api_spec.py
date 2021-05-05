"""OpenAPI v3 Specification"""

# apispec via OpenAPI
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from src.schemas import ApiResponse, SearchResponse, TweetCreate, \
    TweetResponse, TweetId


# Create an APISpec
spec = APISpec(
    title="My Swagger App",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)


# register schemas with spec
spec.components.schema("ApiResponse", schema=ApiResponse)
spec.components.schema("TweetCreate", schema=TweetCreate)
spec.components.schema("TweetResponse", schema=TweetResponse)
spec.components.schema("SearchResponse", schema=SearchResponse)
spec.components.schema("TweetId", schema=TweetId)

# add swagger tags that are used for endpoint annotation
tags = [
    {'name': 'tweet',
     'description': 'Everything about tweets.'
    }
]

for tag in tags:
    print(f"Adding tag: {tag['name']}")
    spec.tag(tag)
