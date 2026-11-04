"""Selection helpers for warm measurement rounds."""

import numpy as np
import numpy.typing as npt

from measurements.processing import validate_shape

FloatArray = npt.NDArray[np.float64]


def select_warm_rounds(readings: FloatArray, threshold: float) -> FloatArray:
    """Return rows whose north-room temperature is at least the threshold."""
    array = np.asarray(readings, dtype=np.float64)
    validate_shape(array)
    if not np.isfinite(array).all():
        raise ValueError("Readings must be finite")
    threshold_value = float(threshold)
    if not np.isfinite(threshold_value):
        raise ValueError("Threshold must be finite")
    selected = array[array[:, 0] >= threshold_value].copy()
    return selected
