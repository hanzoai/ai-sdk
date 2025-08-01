# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel
from .budget_table import BudgetTable

__all__ = ["HanzoEndUserTable"]


class HanzoEndUserTable(BaseModel):
    blocked: bool

    user_id: str

    alias: Optional[str] = None

    allowed_model_region: Optional[Literal["eu", "us"]] = None

    default_model: Optional[str] = None

    hanzo_budget_table: Optional[BudgetTable] = None
    """Represents user-controllable params for a Hanzo_BudgetTable record"""

    spend: Optional[float] = None
