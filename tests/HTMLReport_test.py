import unittest

import HTMLReport


class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        with self.assertRaises(TypeError):
            s.split(2)

    def test_error(self):
        raise ValueError

    def test_fail(self):
        self.assertEqual(1, 2)

    @unittest.skip("This is a skipped test.")
    def test_skip(self):
        pass


if __name__ == '__main__':
    # 测试套件
    suite = unittest.TestSuite()
    # 测试用例加载器
    loader = unittest.TestLoader()
    # 把测试用例加载到测试套件中
    suite.addTests(loader.loadTestsFromTestCase(TestStringMethods))

    # 测试用例执行器
    runner = HTMLReport.TestRunner(report_file_name='test',  # 报告文件名，默认“test”
                                   output_path='report',  # 保存文件夹名，默认“report”
                                   verbosity=2,  # 控制台输出详细程度，默认 2
                                   title='测试报告',  # 报告标题，默认“测试报告”
                                   description='无测试描述',  # 报告描述，默认“无测试描述”
                                   thread_count=2,  # 是否多线程测试（无序执行），默认 1
                                   sequential_execution=True  # 是否按照套件添加(addTests)顺序执行，
                                   # 会等待一个addTests执行完成，再执行下一个，默认 False
                                   )
    # 执行测试用例套件
    runner.run(suite)
