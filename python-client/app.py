from botocore.eventstream import EventStream
import boto3
import json
from patch_credentials_scope import patch_credentials_scope
from endpoint_url import ENDPOINT_URL


def main():
    try:
        session = boto3.Session(region_name="us-east-1")
        runtime = session.client("bedrock-runtime", endpoint_url=ENDPOINT_URL)
        patch_credentials_scope(runtime, session, "lambda")

        result = runtime.invoke_model_with_response_stream(
            body=json.dumps(
                {
                    "inputText": "Hello, Titan",
                    "textGenerationConfig": {
                        "maxTokenCount": 100,
                        "stopSequences": [],
                        "temperature": 0.7,
                        "topP": 0.9,
                    },
                }
            ),
            contentType="application/json",
            accept="*/*",
            modelId="amazon.titan-text-lite-v1",
        )
    except Exception as e:
        print(">>>")
        print(e)
        print("ERR")

    body: EventStream = result.get("body")
    for event in body:
        print(event)


main()
