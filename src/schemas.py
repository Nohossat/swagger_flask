from marshmallow import Schema, fields, validate


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
    # sentiment = fields.Str(validate=validate.OneOf(["undefined", "positive", "negative", "neutral"]))
    # tags = fields.List(fields.Nested(Tag), description="A list of tags to describe the tweet")
    text = fields.String(required=True, validate=validate.Length(max=280), example="L'école permet de lutter contre les inégalités sociales et de destin. C'est pourquoi nos enfants doivent pouvoir continuer à s'y rendre et à apprendre, avec un protocole strict. Bonne rentrée à tous ! Et continuons à appliquer les gestes barrières (souvenons-nous de la chanson).")
    timestamp = fields.DateTime(example="2021-04-26T10:12:58.694Z")
    tweetDate = fields.DateTime(format="%a %b %d %H:%M:%S %z %Y", example="Sat Apr 24 14:01:25 +0000 2021")
    tweetLink = fields.Url(example="https://twitter.com/EmmanuelMacron/status/1385257895240024070")
    twitterId = fields.Str()
    type = fields.Str(example="tweet")


class TweetCreateList(Schema):
    tweets = fields.List(fields.Nested(TweetCreate))


class TweetId(Schema):
    id = fields.Number(description="Tweet Id", required=True, example=2938)


class TweetResponse(Schema):
    id = fields.Int(format="int64", required=True)
    text = fields.String(required=True, validate=validate.Length(max=280),
                         example="L'école permet de lutter contre les inégalités sociales et de destin. C'est pourquoi nos enfants doivent pouvoir continuer à s'y rendre et à apprendre, avec un protocole strict. Bonne rentrée à tous ! Et continuons à appliquer les gestes barrières (souvenons-nous de la chanson).")
    tags = fields.List(fields.Nested(Tag), description="A list of tags to describe the tweet")
    tweetDate = fields.DateTime(example="Mon Apr 26 05:44:19 +0000 2021")
    mediaUrl = fields.List(fields.Url(example="https://pbs.twimg.com/media/Ezvm0HeWQAA0KuW.jpg"))
    sentiment = fields.Str(validate=validate.OneOf(["undefined", "positive", "negative", "neutral"]))


class SearchResponse(Schema):
    results = fields.List(fields.Nested(TweetResponse))


class SearchInput(Schema):
    tags = fields.List(fields.String(validate=validate.Length(max=100), required=True))
