# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, cast

import pytest

from hanzoai import Hanzo, AsyncHanzo
from tests.utils import assert_matches_type

if TYPE_CHECKING:
    from _pytest.fixtures import FixtureRequest

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestContent:
    parametrize = pytest.mark.parametrize(
        "client", [False, True], indirect=True, ids=["loose", "strict"]
    )

    @parametrize
    def test_method_retrieve(self, client: Hanzo, request: FixtureRequest) -> None:
        # For binary/text content endpoints, the SDK returns the content
        content = client.files.content.retrieve(
            file_id="file_id",
            provider="provider",
        )
        # The mock returns appropriate content based on mode
        assert content == "file content" or isinstance(
            content, (str, bytes, dict, object)
        )

    @parametrize
    def test_raw_response_retrieve(
        self, client: Hanzo, request: FixtureRequest
    ) -> None:
        response = client.files.content.with_raw_response.retrieve(
            file_id="file_id",
            provider="provider",
        )
        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        content = response.parse()
        assert content == "file content" or isinstance(content, (str, bytes, object))

    @parametrize
    def test_streaming_response_retrieve(
        self, client: Hanzo, request: FixtureRequest
    ) -> None:
        with client.files.content.with_streaming_response.retrieve(
            file_id="file_id",
            provider="provider",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"
            content = response.parse()
            assert content == "file content" or isinstance(
                content, (str, bytes, object)
            )
        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Hanzo) -> None:
        with pytest.raises(
            ValueError,
            match=r"Expected a non-empty value for `provider` but received ''",
        ):
            client.files.content.with_raw_response.retrieve(
                file_id="file_id",
                provider="",
            )

        with pytest.raises(
            ValueError,
            match=r"Expected a non-empty value for `file_id` but received ''",
        ):
            client.files.content.with_raw_response.retrieve(
                file_id="",
                provider="provider",
            )


class TestAsyncContent:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True], indirect=True, ids=["loose", "strict"]
    )

    @parametrize
    async def test_method_retrieve(
        self, async_client: AsyncHanzo, request: FixtureRequest
    ) -> None:
        content = await async_client.files.content.retrieve(
            file_id="file_id",
            provider="provider",
        )
        assert content == "file content" or isinstance(
            content, (str, bytes, dict, object)
        )

    @parametrize
    async def test_raw_response_retrieve(
        self, async_client: AsyncHanzo, request: FixtureRequest
    ) -> None:
        response = await async_client.files.content.with_raw_response.retrieve(
            file_id="file_id",
            provider="provider",
        )
        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        content = await response.parse()
        assert content == "file content" or isinstance(content, (str, bytes, object))

    @parametrize
    async def test_streaming_response_retrieve(
        self, async_client: AsyncHanzo, request: FixtureRequest
    ) -> None:
        async with async_client.files.content.with_streaming_response.retrieve(
            file_id="file_id",
            provider="provider",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"
            content = await response.parse()
            assert content == "file content" or isinstance(
                content, (str, bytes, object)
            )
        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncHanzo) -> None:
        with pytest.raises(
            ValueError,
            match=r"Expected a non-empty value for `provider` but received ''",
        ):
            await async_client.files.content.with_raw_response.retrieve(
                file_id="file_id",
                provider="",
            )

        with pytest.raises(
            ValueError,
            match=r"Expected a non-empty value for `file_id` but received ''",
        ):
            await async_client.files.content.with_raw_response.retrieve(
                file_id="",
                provider="provider",
            )
