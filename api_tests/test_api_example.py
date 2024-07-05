# api_tests/test_api_example.py



import sys
import os
# 将 utils 目录添加到模块搜索路径中
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'common')))

import pytest
import requests
from common.helpers import assert_equal
from common.config import API_BASE_URL

@pytest.mark.api
def test_api_example():
    response = requests.get(API_BASE_URL)
    assert_equal(response.status_code, 200)
