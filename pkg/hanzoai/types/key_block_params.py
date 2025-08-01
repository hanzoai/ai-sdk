# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["KeyBlockParams"]


class KeyBlockParams(TypedDict, total=False):
    key: Required[str]

    hanzo_changed_by: Annotated[str, PropertyInfo(alias="hanzo-changed-by")]
    """
    The hanzo-changed-by header enables tracking of actions performed by
    authorized users on behalf of other users, providing an audit trail for
    accountability
    """
