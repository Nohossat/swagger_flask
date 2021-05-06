from flask import Blueprint, jsonify, request
from marshmallow import ValidationError, EXCLUDE, pre_load

from src.schemas import TweetCreateList, TweetId, \
    SearchInput, ApiResponse, UpdateInput, TweetResponseList, TweetResponse
from src.sqlite.db import insert_tweets, get_tweet_from_id, \
    delete_tweet_from_id, get_sentiment_to_tweet_from_id, get_all_tweet

# CONTROLLER

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
              schema: TweetResponseList
        '400':
          description: Cannot insert the new tweets
          content:
            application/json:
              schema: ApiResponse
      tags:
          - tweet
    """
    data = request.get_json()
    schema = TweetCreateList()
    error_response_schema = ApiResponse()
    response_schema = TweetResponseList()
    response = None
    code = None

    try:
        tweets = schema.load(data)
        results = insert_tweets(tweets["tweets"])
        response = {"tweets": results}
        response = response_schema.load(response)
    except ValidationError as e:
        code = 400
        response = error_response_schema.load({
            "code": code,
            "type": "Validation error",
            "msg": str(e)
        })
    except ValueError as e:
        code = 400
        response = error_response_schema.load({
            "code": code,
            "type": "Value Error",
            "msg": str(e)
        })

    return response, code


@tweet.route('/<id>', methods=['GET'])
def get_tweet(id):  # noqa: E501
    """
    ---
    get:
      description: Fetch a tweet from the database
      parameters:
      - name: id
        in: path
        schema: TweetId
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
    error_response_schema = ApiResponse()
    response_schema = TweetResponse(unknown=EXCLUDE)
    response = None
    code = None

    try:
        schema.load({'id': id})
        response_db = get_tweet_from_id(id)
        response = response_schema.load(response_db)
        code = 200
    except ValidationError as e:
        code = 400
        response = error_response_schema.load({
            "code": code,
            "type": "Validation error",
            "msg": str(e)
        })
    except ValueError as e:
        code = 404
        response = error_response_schema.load({
            "code": code,
            "type": "Not found",
            "msg": str(e)
        })

    return response, code


@tweet.route('/tweets', methods=['GET'])
def get_all_tweets():  # noqa: E501
    """
    ---
    get:
      description: Fetch all tweets

      responses:
        '200':
          description: Get all tweets in database
          content:
            application/json:
              schema: TweetResponse
        '404':
          description: Tweets not found
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

    error_response_schema = ApiResponse()
    response_schema = TweetResponseList(unknown=EXCLUDE)
    response = None
    code = None

    try:
        response_db = get_all_tweet()
        print(response_db, flush=True)
        response = response_schema.load(response_db)
        code = 200
    except ValidationError as e:
        code = 400
        response = error_response_schema.load({
            "code": code,
            "type": "Validation error",
            "msg": str(e)
        })
    except ValueError as e:
        code = 404
        response = error_response_schema.load({
            "code": code,
            "type": "Not found",
            "msg": str(e)
        })

    return response, code


@tweet.route('/<id>', methods=['PUT'])
def update_tweet(id):  # noqa: E501
    """
    ---
    put:
      description: Update a tweet sentiment
      parameters:
      - name: id
        in: path
        description: Tweet Id
        schema: TweetId

      responses:
        '200':
          description: Get complete Tweet
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
    error_response_schema = ApiResponse()
    response_schema = TweetResponse(unknown=EXCLUDE)
    response = None
    code = None

    try:
        input = schema.load({'id': id})
        response = get_sentiment_to_tweet_from_id(id)
        response = response_schema.load(response)
        code = 200
    except ValidationError as e:
        code = 400
        response = error_response_schema.load({
            "code": code,
            "type": "Validation error",
            "msg": str(e)
        })
    except ValueError as e:
        code = 404
        response = error_response_schema.load({
            "code": code,
            "type": "Not found",
            "msg": str(e)
        })
    return response, code


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
    response = None
    code = None

    try:
        schema.load({'id': id})
        code = 200
        response = response_schema.load({
            "code": code,
            "type": "Tweet deletion",
            "msg": str(delete_tweet_from_id(id))
        })
    except ValidationError as e:
        code = 400
        response = response_schema.load({
            "code": code,
            "type": "Validation error",
            "msg": str(e)
        })
        return response
    except ValueError as e:
        code = 404
        response = response_schema.load({
            "code": code,
            "type": "Not found",
            "msg": str(e)
        })
    return response, code


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