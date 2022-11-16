import pytest
import boa
import boa.test
import hypothesis


_old_init = hypothesis.core.HypothesisHandle.__init__
def _HypothesisHandle__init__(self, *args, **kwargs):
    _old_init(self, *args, **kwargs)

    t = self.inner_test

    def f(*args, **kwargs):
        with boa.env.anchor():
            t(*args, **kwargs)

    self.inner_test = f

#hypothesis.core.HypothesisHandle.__init__ = _HypothesisHandle__init__


def pytest_configure(config):
    config.addinivalue_line("markers", "ignore_isolation")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item: pytest.Item) -> None:

    if not item.get_closest_marker("ignore_isolation"):
        with boa.env.anchor():
            yield
    else:
        yield