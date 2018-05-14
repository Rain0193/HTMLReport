import base64
import logging
import unittest

import HTMLReport
from HTMLReport import AddImage
from HTMLReport import logger


def parse_int(s):
    return int(s)


LOG = logging.getLogger(__name__)


class test_1th(unittest.TestCase):
    def test_isupper(self):
        """测试isupper"""
        logger().info("测试isupper")
        LOG.info("11111111111111111111111111111111111111111111111111111")
        self.assertTrue('FOO'.isupper(), "真")
        self.assertFalse('Foo'.isupper(), '假')

    def test_split(self):
        """测试split"""
        logger().info("测试split")
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'], "相等")
        with self.assertRaises(TypeError):
            s.split(2)

    def test_error(self):
        """测试错误"""
        logger().error("测试错误")
        with open("baidu.png", 'rb') as f:
            image = base64.b64encode(f.read())
            AddImage(image, "百度1")
            AddImage(image, "百度12")
            AddImage(image, "百度123")
        raise ValueError

    def test_fail(self):
        """测试失败"""
        logger().info("测试失败")
        self.assertEqual(1, 2, "相等")

    @unittest.skip("这是一个跳过的测试")
    def test_skip(self):
        """测试跳过"""
        logger().warning("测试跳过")
        pass


class test_2th(unittest.TestCase):
    def test_bad_int(self):
        """测试异常类型"""
        logger().info("测试异常类型")
        self.assertRaises(ValueError, parse_int("1.5"), 'N/A')

    def test_upper(self):
        """测试相等"""
        logger().critical('测试相等')
        self.assertEqual('foo'.upper(), '00')


class test_第三个测试(unittest.TestCase):
    a = None

    @classmethod
    def setUpClass(cls):
        """公共"""
        cls.a = 1
        LOG.info("a : {}".format(cls.a))

    @classmethod
    def tearDownClass(cls):
        LOG.info("a : {}".format(cls.a))

    def test_True(self):
        """测试True"""
        test_第三个测试.a += 1
        self.assertTrue(False, self.a)

    def test_False(self):
        """测试FALSE"""
        test_第三个测试.a += 1
        self.assertFalse(True, self.a)


if __name__ == '__main__':
    # 测试套件
    suite = unittest.TestSuite()
    # 测试用例加载器
    loader = unittest.TestLoader()
    # 把测试用例加载到测试套件中
    suite.addTests(loader.loadTestsFromTestCase(test_1th))
    suite.addTests(loader.loadTestsFromTestCase(test_2th))
    suite.addTests(loader.loadTestsFromTestCase(test_第三个测试))

    # 测试用例执行器
    runner = HTMLReport.TestRunner(report_file_name='test',  # 报告文件名，如果未赋值，将采用“test+时间戳”
                                   output_path='report',  # 保存文件夹名，默认“report”
                                   title='一个简单的测试报告',  # 报告标题，默认“测试报告”
                                   description='随意描述',  # 报告描述，默认“无测试描述”
                                   thread_count=2,  # 并发线程数量（无序执行测试），默认数量 1
                                   thread_start_wait=0,  # 各线程启动延迟，默认 0 s
                                   sequential_execution=True,  # 是否按照套件添加(addTests)顺序执行，
                                   # 会等待一个addTests执行完成，再执行下一个，默认 False
                                   # 如果用例中存在 tearDownClass ，建议设置为True，
                                   # 否则 tearDownClass 将会在所有用例线程执行完后才会执行。
                                   # lang='en'
                                   lang='cn'  # 支持中文与英文，默认中文
                                   )
    # 执行测试用例套件
    runner.run(suite)
