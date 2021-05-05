from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

# import connexion
import six

from src.models.api_response import ApiResponse  # noqa: E501
from src.models.search_response import SearchResponse  # noqa: E501
from src.models.tweet_create import TweetCreate  # noqa: E501
from src.models.tweet_response import TweetResponse  # noqa: E501

from src.schemas import TweetCreateList, TweetId, SearchInput, ApiResponse
from src.sqlite.queries import create_connection, insert_tweets, get_tweet_from_id, \
    delete_tweet_from_id, update_tweet_from_id

tweet = Blueprint(name="tweet", import_name=__name__)


@tweet.route('/', methods=['POST'])
def post_tweet(body=None):  # noqa: E501
    """
    ---
    post:
      description: Analyze a list of tweets sentiments and store them in database
      requestBody:
        required: true
        content:
            application/json:
                schema: TweetCreateList

      responses:
        '200':
          description: Compute sentiment for a tweet
          content:
            application/json:
              schema: TweetResponse
        '404':
          description: Invalid tweet id
          content:
            application/json:
              schema: TweetResponse
      tags:
          - tweet
    """
    data = request.get_json()
    schema = TweetCreateList()
    response_schema = ApiResponse()

    try:
        tweets = schema.load(data)
        print(data, flush=True)
        # print(tweets["tweets"], flush=True)
        create_connection(insert_tweets, tweets["tweets"])
        return tweets
        # TODO return the inserted posts
    except ValidationError as e:
        response = response_schema.load({
            "code": 400,
            "type": "Validation error",
            "message": str(e)
        })
        return response


@tweet.route('/<id>', methods=['GET'])
def get_tweet(id):  # noqa: E501
    """
    ---
    get:
      description: Fetch a tweet from the database
      parameters:
      - name: id
        in: path
        type: string
        required: true
        description: Tweet Id

      responses:
        '200':
          description: Get complete tweet
          content:
            application/json:
              schema: TweetResponse
        '404':
          description: Tweet not found
          content:
            application/json:
              schema: ApiResponse
        '400':
          description: Validation error
          content:
            application/json:
              schema: ApiResponse

      tags:
          - tweet
    """
    schema = TweetId()
    response_schema = ApiResponse()

    try:
        schema.load({'id': id})
        response = create_connection(get_tweet_from_id, id) # utiliser un décorateur
        return str(response)
    except ValidationError as e:
        response = response_schema.load({
            "code": 400,
            "type": "Validation error",
            "message": str(e)
        })
        return response
    except ValueError as e:
        response = response_schema.load({
            "code": 404,
            "type": "Not found",
            "message": str(e)
        })
        return response


@tweet.route('/<id>', methods=['PUT'])
def update_tweet(id):  # noqa: E501
    """
    ---
    put:
      description: Update a tweet sentiment
      parameters:
      - name: id
        in: path
        type: string
        required: true
        description: Tweet Id

      responses:
        '200':
          description: Get complte Tweet
          content:
            application/json:
              schema: TweetResponse

        '400':
          description: Invalid ID supplied
          content:
            application/json:
              schema: ApiResponse

        '404':
          description: Tweet not found
          content:
            application/json:
              schema: ApiResponse

        '405':
          description: Validation exception
          content:
            application/json:
              schema: ApiResponse
      tags:
          - tweet
    """
    schema = TweetId()
    response_schema = ApiResponse()

    try:
        schema.load({'id': id})
        response = create_connection(update_tweet_from_id, id)  # utiliser un décorateur
        return str(response)
    except ValidationError as e:
        response = response_schema.load({
            "code": 400,
            "type": "Validation error",
            "message": str(e)
        })
        return response
    except ValueError as e:
        response = response_schema.load({
            "code": 404,
            "type": "Not found",
            "message": str(e)
        })
        return response


@tweet.route('/<id>', methods=['DELETE'])
def delete_tweet(id):  # noqa: E501
    """
     ---
    delete:
      description: Deletes a tweet
      parameters:
        - name: id
          in: path
          description: Deletes a tweet in the database # noqa: E501
          schema: TweetId

      responses:
        '200':
          description: Deletion confirmation
          content:
            application/json:
              schema: ApiResponse

        '400':
          description: Invalid ID supplied
          content:
            application/json:
              schema: ApiResponse

        '404':
          description: Tweet not found
          content:
            application/json:
              schema: ApiResponse
      tags:
          - tweet
    """

    schema = TweetId()
    response_schema = ApiResponse()

    try:
        schema.load({'id': id})
        response = create_connection(delete_tweet_from_id, id)  # utiliser un décorateur
        return str(response)
    except ValidationError as e:
        response = response_schema.load({
            "code": 400,
            "type": "Validation error",
            "message": str(e)
        })
        return response
    except ValueError as e:
        response = response_schema.load({
            "code": 404,
            "type": "Not found",
            "message": str(e)
        })
        return response


@tweet.route('/search', methods=['GET'])
def search_tweet():  # noqa: E501
    """Fetch tweets from the database
     ---
    get:
      description: Query tweets from a list of tags (separated by comma) # noqa: E501
      parameters:
        - name: tags
          in: query
          schema:
            type: array
            items: String
            example: ["macron", "election", "covid"]

      responses:
        '200':
          description: Tweets found
          content:
            application/json:
              schema: ApiResponse

        '404':
          description: Tweets not found
          content:
            application/json:
              schema: ApiResponse
      tags:
          - tweet
    """

    # TODO : replace with request to sqlite
    schema = SearchInput()
    tags = request.args.getlist('tags')

    try:
        result = schema.load({'tags': tags})
    except ValidationError as e:
        return f"Validation errors: {e}", 400
    return result