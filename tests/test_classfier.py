import yalm
import pytest

@pytest.mark.parametrize(
    'license_id,sample_key', 
    [(lic.id, s.key) for lic in yalm.spdx_licenses.values() for s in lic.positive_samples]
)
def test_positive_samples(license_id, sample_key):
    sample = yalm.spdx_licenses[license_id].positive_sample(sample_key).document
    assert license_id == yalm.detect_license(sample).template.id
