"""
tests/test_ocr_mineru_gpu_pin.py
[[tests.test_ocr_mineru_gpu_pin]]
https://github.com/Mjvolk3/Swanki/tree/main/tests/test_ocr_mineru_gpu_pin.py

MinerU GPU-pin resolution: honor an explicit config pin, else inherit the
ambient CUDA_VISIBLE_DEVICES (SLURM allocates one GPU as local index 0). Guards
against the old hardcoded "3" that is out of range inside a 1-GPU cgroup.
"""

from swanki.ocr.mineru import _ocr_gpu_pin


def test_unset_config_inherits_ambient():
    assert _ocr_gpu_pin({}) is None


def test_explicit_none_inherits_ambient():
    assert _ocr_gpu_pin({"cuda_visible_devices": None}) is None


def test_empty_string_inherits_ambient():
    assert _ocr_gpu_pin({"cuda_visible_devices": ""}) is None


def test_no_implicit_gpu_three_default():
    # The legacy default was "3"; under SLURM that is out of range. Absence of a
    # pin must mean "inherit", never a baked-in index.
    assert _ocr_gpu_pin({}) != "3"


def test_explicit_string_pin_honored():
    assert _ocr_gpu_pin({"cuda_visible_devices": "2"}) == "2"


def test_explicit_int_pin_coerced_to_str():
    assert _ocr_gpu_pin({"cuda_visible_devices": 1}) == "1"
