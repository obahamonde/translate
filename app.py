from boto3 import Session
from fastapi import FastAPI
from dotenv import load_dotenv
from os import environ
from mangum import Mangum
load_dotenv()

AWS_ACCESS_KEY_ID = environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = environ['AWS_ACCESS_KEY_ID']
AWS_DEFAULT_REGION = environ['AWS_DEFAULT_REGION']

app = FastAPI()

class Aws(Session):
    def __init__(self):
        super().__init__(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_DEFAULT_REGION
        )
    
    @property
    def translate(self):
        return self.client('translate')


@app.get('/translate/{text}')
async def translate(text: str, source: str = 'en', target: str = 'es'):
    aws = Aws()
    response = aws.translate.translate_text(
        Text=text,
        SourceLanguageCode=source,
        TargetLanguageCode=target
    )
    response.pop('ResponseMetadata')
    return response

handler = Mangum(app)
