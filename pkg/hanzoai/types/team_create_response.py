# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from .member import Member
from .._models import BaseModel
<<<<<<<< HEAD:pkg/hanzoai/types/team_create_response.py

__all__ = ["TeamCreateResponse", "LlmModelTable"]


class LlmModelTable(BaseModel):
    created_by: str

    updated_by: str

    api_model_aliases: Union[str, object, None] = FieldInfo(alias="model_aliases", default=None)


class TeamCreateResponse(BaseModel):
========
from .lite_llm_model_table import HanzoModelTable

__all__ = ["HanzoTeamTable"]


class HanzoTeamTable(BaseModel):
>>>>>>>> 870084b (Update python monorepo):pkg/hanzoai/types/lite_llm_team_table.py
    team_id: str

    admins: Optional[List[object]] = None

    blocked: Optional[bool] = None

    budget_duration: Optional[str] = None

    budget_reset_at: Optional[datetime] = None

    created_at: Optional[datetime] = None

<<<<<<<< HEAD:pkg/hanzoai/types/team_create_response.py
    llm_model_table: Optional[LlmModelTable] = None
========
    hanzo_model_table: Optional[HanzoModelTable] = None
>>>>>>>> 870084b (Update python monorepo):pkg/hanzoai/types/lite_llm_team_table.py

    max_budget: Optional[float] = None

    max_parallel_requests: Optional[int] = None

    members: Optional[List[object]] = None

    members_with_roles: Optional[List[Member]] = None

    metadata: Optional[object] = None

    api_model_id: Optional[int] = FieldInfo(alias="model_id", default=None)

    models: Optional[List[object]] = None

    organization_id: Optional[str] = None

    rpm_limit: Optional[int] = None

    spend: Optional[float] = None

    team_alias: Optional[str] = None

    tpm_limit: Optional[int] = None
