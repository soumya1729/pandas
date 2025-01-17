"""
This file contains a minimal set of tests for compliance with the extension
array interface test suite, and should contain no other tests.
The test suite for the full functionality of the array is located in
`pandas/tests/arrays/`.

The tests in this file are inherited from the BaseExtensionTests, and only
minimal tweaks should be applied to get the tests passing (by overwriting a
parent method).

Additional tests should either be added to one of the BaseExtensionTests
classes (if they are relevant for the extension interface for all dtypes), or
be added to the array-specific tests in `pandas/tests/arrays/`.

"""
import numpy as np
import pytest

from pandas._libs import iNaT
from pandas.compat import is_platform_windows
from pandas.compat.numpy import np_version_gte1p24

from pandas.core.dtypes.dtypes import PeriodDtype

import pandas as pd
import pandas._testing as tm
from pandas.core.arrays import PeriodArray
from pandas.tests.extension import base


@pytest.fixture(params=["D", "2D"])
def dtype(request):
    return PeriodDtype(freq=request.param)


@pytest.fixture
def data(dtype):
    return PeriodArray(np.arange(1970, 2070), dtype=dtype)


@pytest.fixture
def data_for_twos(dtype):
    pytest.skip("Not a numeric dtype")


@pytest.fixture
def data_for_sorting(dtype):
    return PeriodArray([2018, 2019, 2017], dtype=dtype)


@pytest.fixture
def data_missing(dtype):
    return PeriodArray([iNaT, 2017], dtype=dtype)


@pytest.fixture
def data_missing_for_sorting(dtype):
    return PeriodArray([2018, iNaT, 2017], dtype=dtype)


@pytest.fixture
def data_for_grouping(dtype):
    B = 2018
    NA = iNaT
    A = 2017
    C = 2019
    return PeriodArray([B, B, NA, NA, A, A, B, C], dtype=dtype)


@pytest.fixture
def na_value():
    return pd.NaT


class BasePeriodTests:
    pass


class TestPeriodDtype(BasePeriodTests, base.BaseDtypeTests):
    pass


class TestConstructors(BasePeriodTests, base.BaseConstructorsTests):
    pass


class TestGetitem(BasePeriodTests, base.BaseGetitemTests):
    pass


class TestIndex(base.BaseIndexTests):
    pass


class TestMethods(BasePeriodTests, base.BaseMethodsTests):
    @pytest.mark.parametrize("periods", [1, -2])
    def test_diff(self, data, periods):
        if is_platform_windows() and np_version_gte1p24:
            with tm.assert_produces_warning(RuntimeWarning, check_stacklevel=False):
                super().test_diff(data, periods)
        else:
            super().test_diff(data, periods)

    @pytest.mark.parametrize("na_action", [None, "ignore"])
    def test_map(self, data, na_action):
        result = data.map(lambda x: x, na_action=na_action)
        tm.assert_extension_array_equal(result, data)


class TestInterface(BasePeriodTests, base.BaseInterfaceTests):
    pass


class TestArithmeticOps(BasePeriodTests, base.BaseArithmeticOpsTests):
    def _get_expected_exception(self, op_name, obj, other):
        if op_name in ("__sub__", "__rsub__"):
            return None
        return super()._get_expected_exception(op_name, obj, other)


class TestCasting(BasePeriodTests, base.BaseCastingTests):
    pass


class TestComparisonOps(BasePeriodTests, base.BaseComparisonOpsTests):
    pass


class TestMissing(BasePeriodTests, base.BaseMissingTests):
    pass


class TestReshaping(BasePeriodTests, base.BaseReshapingTests):
    pass


class TestSetitem(BasePeriodTests, base.BaseSetitemTests):
    pass


class TestGroupby(BasePeriodTests, base.BaseGroupbyTests):
    pass


class TestPrinting(BasePeriodTests, base.BasePrintingTests):
    pass


class TestParsing(BasePeriodTests, base.BaseParsingTests):
    pass


class Test2DCompat(BasePeriodTests, base.NDArrayBacked2DTests):
    pass
