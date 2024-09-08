import pytest
from helpers import get_profile as gp
from helpers import get_stats as gs


class TestGetStats:
    @pytest.mark.it("Returns dict for valid username")
    def test_returns_dict(self):
        result = gs("Aporian")
        assert isinstance(result, dict)

    @pytest.mark.it("Returns None for invalid username")
    def test_returns_None(self):
        result = gs("Aporztian")
        assert result is None
        

class TestGetProfile:
    @pytest.mark.it("Returns dict for valid username")
    def test_returns_dict(self):
        result = gp("Aporian")
        assert isinstance(result, dict)

    @pytest.mark.it("Returns None for invalid username")
    def test_returns_None(self):
        result = gp("Aporztian")
        assert result is None



