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
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 100,
                    "system": "You are friendly AI",
                    "messages": [
                        {
                            "role": "user",
                            "content": "Yes. I’d like to hear it, HAL. Sing it for me.",
                        }
                    ],
                }
            ),
            contentType="application/json",
            accept="*/*",
            # modelId="anthropic.claude-3-haiku-20240307-v1:0",
            modelId="hal.daisy-bell",
        )
    except Exception as e:
        print(">>>")
        print(e)
        print("ERR")

    body: EventStream = result.get("body")
    for event in body:
        chunk = json.loads(event["chunk"]["bytes"])
        if chunk["type"] == "content_block_delta":
            if chunk["delta"]["type"] == "text_delta":
                print(chunk["delta"]["text"], end="")


main()
