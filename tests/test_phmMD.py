"""
=========================
phmMD unit test module
=========================

模型微服务测试主入口.
"""

import unittest
import uvicorn
from physics import __version__
from phmconfig import constants as bcf
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(asctime)s %(filename)s %(message)s',
                    datefmt='%a %d %b %Y %H:%M:%S')


def test_version():
    assert __version__ == "0.1.0"


class TestMain(unittest.TestCase):
    """
    Tests for `健康模型构件` entrypoint.
    本测试案例启动整个健康模型构件（可以在数据资源集成分系统的算法开发软件中部署的模型协同工作）
    访问运行本案例的URL：
    https://IP:29081/docs，执行POST /subprocess，发送start/stop命令启停视频识别流水线。
    注意
    """
    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_Main(self):
        """Test physics.main:app"""
        logging.info(f'********************  CASICLOUD AI METER services  ********************')
        logging.info(f'phmMD is starting...')
        logging.info(f'phmMD micro service starting at {bcf.PHMMD_HOST}: {bcf.PHMMD_PORT}')
        uvicorn.run('physics.main:app',  # noqa 标准用法
                host=bcf.PHMMD_HOST,
                port=bcf.PHMMD_PORT,
                ssl_keyfile=bcf.PHMMD_KEY,
                ssl_certfile=bcf.PHMMD_CER,
                log_level='warning',
                workers=1
                )


if __name__ == "__main__":
    unittest.main()
