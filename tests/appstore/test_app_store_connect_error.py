from maker.appstore import AppStoreConnectError, AppStoreConnectErrorResponse


def test_it_errors_empty():
    err = {"errors": []}
    actual = AppStoreConnectError(err=err)

    assert actual.errors == []


def test_it_errors_exists():
    err = {
        "errors": [
            {
                "code": "stub code",
                "status": "stub status",
                "id": None,
                "title": "stub title",
                "detail": "stub detail",
            },
            {
                "code": "stub code",
                "status": "stub status",
                "title": "stub title",
                "detail": "stub detail",
            },
            {
                "code": "stub code",
                "status": "stub status",
                "id": "stub id",
                "title": "stub title",
                "detail": "stub detail",
            },
        ]
    }
    actual = AppStoreConnectError(err=err)

    assert actual.errors == [
        AppStoreConnectErrorResponse(
            status="stub status",
            code="stub code",
            id_=None,
            title="stub title",
            detail="stub detail",
        ),
        AppStoreConnectErrorResponse(
            status="stub status",
            code="stub code",
            id_=None,
            title="stub title",
            detail="stub detail",
        ),
        AppStoreConnectErrorResponse(
            status="stub status",
            code="stub code",
            id_="stub id",
            title="stub title",
            detail="stub detail",
        ),
    ]
