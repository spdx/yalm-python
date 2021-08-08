import yalm
import pytest


@pytest.mark.parametrize(
    'license_id', list(map(lambda x: x.id, yalm.spdx_licenses))
)
def test_classfier_positive(license_id):
    assert license_id != 'MIT'
