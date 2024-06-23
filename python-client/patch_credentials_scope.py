from botocore.awsrequest import AWSPreparedRequest, AWSRequest
from botocore.auth import SigV4Auth
from botocore.httpsession import URLLib3Session

_request: AWSRequest = None


def patch_credentials_scope(runtime, session, service_name: str):
    """
    boto3がリクエストする認証スコープを書き変える
    """
    # イベントのハンドラを取得する
    event_system = runtime.meta.events

    # 署名の直前に呼ばれる関数を定義する
    def _ref_request(request: AWSRequest, **kwargs):
        # 署名前の送信情報を参照する
        global _request
        _request = request

    # API送信の直前に呼ばれる関数を定義する
    def _before_send(request: AWSPreparedRequest, **kwargs):
        # ここで受け取るrequestはprepareでURLエンコードされているので、
        # 署名前の送信情報を元に再署名をする

        # ヘッダの型をstr: strに整形する
        def header_item_from_prepare_request(item):
            if isinstance(item, bytes):
                return item.decode()
            return item

        # 署名に使う情報をあらためて詰め直す
        requester = AWSRequest(
            url=_request.url,
            method=_request.method,
            headers={
                k: header_item_from_prepare_request(h)
                for k, h in _request.headers.items()
            },
            data=_request.body.decode(),
            stream_output=request.stream_output,
        )
        # SigV4で署名する
        # service_nameがクレデンシャルスコープになるので、ここを書き変える
        SigV4Auth(
            session.get_credentials(), service_name, session.region_name
        ).add_auth(requester)

        # 送信処理を実行。この関数の実行結果がboto3の実行結果になる
        return URLLib3Session().send(requester.prepare())

    # boto3の割り込みのハンドラを登録する
    # ハンドラの一覧: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/events.html
    event_system.register("before-send.*", _before_send)
    event_system.register_first("before-sign.*", _ref_request)
