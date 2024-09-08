import pytest
from helpers import get_profile as gp


@pytest.mark.it("Returns dict for valid username")
def test_returns_dict():
    result = gp("Aporian")
    assert isinstance(result, dict)


@pytest.mark.it("Returns None for invalid username")
def test_returns_None():
    result = gp("Aporztian")
    assert result is None



