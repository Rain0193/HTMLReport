# HTMLReport

`HTMLReport`是一个单元测试测试运行器，可以将测试结果保存在Html文件中，用于人性化的结果显示。<br><br>仅支持**Python 3.x**

> 多线程不支持 @classmethod 装饰器！采用单线程模式工作！

# 安装
要安装HTMLReport，请在终端中运行此命令
```py
$ pip install HTMLReport
```
这是安装HTMLReport的首选方法，因为它将始终安装最新的稳定版本。如果您没有安装[pip](https://pip.pypa.io/)，则该[Python安装指南](http://docs.python-guide.org/en/latest/starting/installation/ "Python安装指南")可以指导您完成该过程。

# 使用方法
```py
import unittest
import HTMLReport


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
                               thread_count=1,  # 并发线程数量（无序执行测试），默认数量 1
                               sequential_execution=True  # 是否按照套件添加(addTests)顺序执行，
                               # 会等待一个addTests执行完成，再执行下一个，默认 False
                               )
# 执行测试用例套件
runner.run(suite)
```

Links:
---------
* [https://github.com/liushilive/HTMLReport](https://github.com/liushilive/HTMLReport "Github")