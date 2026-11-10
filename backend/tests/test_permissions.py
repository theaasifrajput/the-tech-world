from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.core.permissions import require_admin


def test_admin_user_is_allowed():
    user = SimpleNamespace(role="admin")
    assert require_admin(user) is user


def test_student_user_is_forbidden():
    user = SimpleNamespace(role="student")
    with pytest.raises(HTTPException) as exc:
        require_admin(user)
    assert exc.value.status_code == 403
    assert exc.value.detail == "Administrator access required"
