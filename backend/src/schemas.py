from marshmallow import Schema, fields, validate, EXCLUDE, pre_load


# Define schemas
class InputSchema(Schema):
    number = fields.Int(description="An integer.", required=True)


class OutputSchema(Schema):
    msg = fields.String(description="A message.", required=True)
    code = fields.Integer(description="Test", required=True)


class ApiResponse(Schema):
    code = fields.Integer(description="200", required=True)
    type = fields.String(description="Type")
    msg = fields.String(description="A message.")


class Tag(Schema):
    name = fields.String(example="macron")


class TweetCreate(Schema):
    handle = fields.Str()
    mediaUrl = fields.List(fields.Url(example="https://pbs.twimg.com/media/Ezvm0HeWQAA0KuW.jpg"))
    name = fields.Str(example="Emmanuel Macron")
    profileUser = fields.Url(example="https://twitter.com/EmmanuelMacron")
    query = fields.Url(example="https://twitter.com/EmmanuelMacron")
    sentiment = fields.Str(default="undefined", validate=validate.OneOf(["undefined", "positive", "negative", "neutral"]))
    text = fields.String(required=True, validate=validate.Length(max=500), example="L'école permet de lutter contre les inégalités sociales et de destin. C'est pourquoi nos enfants doivent pouvoir continuer à s'y rendre et à apprendre, avec un protocole strict. Bonne rentrée à tous ! Et continuons à appliquer les gestes barrières (souvenons-nous de la chanson).")
    timestamp = fields.DateTime(example="2021-04-26T10:12:58.694Z")
    tweetDate = fields.DateTime(format="%a %b %d %H:%M:%S %z %Y", example="Sat Apr 24 14:01:25 +0000 2021")
    tweetLink = fields.Url(example="https://twitter.com/EmmanuelMacron/status/1385257895240024070")
    twitterId = fields.Int(example=1976143068)
    type = fields.Str(example="tweet")

    @pre_load
    def add_default_sentiment(self, data, **kwargs):
        if 'sentiment' not in data.keys():
            data["sentiment"] = "undefined"
        return data


class TweetCreateList(Schema):
    tweets = fields.List(fields.Nested(TweetCreate))


class TweetId(Schema):
    id = fields.Number(description="Tweet Id", required=True, example=29)


class TweetResponse(Schema):
    id = fields.Int(format="int64", required=True)
    name = fields.Str(example="Emmanuel Macron")
    query = fields.Url(example="https://twitter.com/EmmanuelMacron")
    text = fields.String(required=True, validate=validate.Length(max=500),
                         example="L'école permet de lutter contre les inégalités sociales et de destin. C'est pourquoi nos enfants doivent pouvoir continuer à s'y rendre et à apprendre, avec un protocole strict. Bonne rentrée à tous ! Et continuons à appliquer les gestes barrières (souvenons-nous de la chanson).")
    tweetDate = fields.DateTime(example="Mon Apr 26 05:44:19 +0000 2021")
    sentiment = fields.Str(missing="undefined", validate=validate.OneOf(["undefined", "positive", "negative", "neutral"]))

    @pre_load
    def default_sentiment(self, data, **kwargs):
        if data["sentiment"] is None:
            data["sentiment"] = "undefined"
        return data


class TweetResponseList(Schema):
    tweets = fields.List(fields.Nested(TweetResponse(unknown=EXCLUDE)))


class SearchResponse(Schema):
    results = fields.List(fields.Nested(TweetResponse))


class SearchInput(Schema):
    tags = fields.List(fields.String(validate=validate.Length(max=100), required=True))


class UpdateInput(Schema):
    id = fields.Int(format="int64", required=True)
    sentiment = fields.Str(required=True, validate=validate.OneOf(["undefined", "positive", "negative", "neutral"]))
