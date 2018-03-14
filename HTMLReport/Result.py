from io import StringIO
from unittest import TestResult

from HTMLReport.log.HandlerFactory import HandlerFactory
from HTMLReport.log.logger import GeneralLogger


class Result(TestResult):
    """
    定义继承自 unittest.TestResult 的 类。
    这里重写了 unittest.TestResult 的多个方法，比如 startTest(self, test) 等等
    """

    def __init__(self, verbosity=2):
        TestResult.__init__(self)
        super().__init__(verbosity)
        self.success_count = 0
        self.failure_count = 0
        self.skip_count = 0
        self.error_count = 0
        self.stderr_steams = StringIO()
        self.stderr_steams.write("\n")
        self.stdout_steams = StringIO()
        self.stdout_steams.write("\n")
        """
        返回结果是一个4个属性的元组的列表
        (
          result code (0: success; 1: fail; 2: error; 3: skip),
          TestCase object,
          Test output (byte string),
          stack trace,
        )
        """
        self.result = []

    def addSkip(self, test, reason):
        self.skip_count += 1
        TestResult.addSkip(self, test, reason)
        self.stderr_steams.write('Skip\t')
        self.stderr_steams.write(str(test))
        doc = test._testMethodDoc
        if doc:
            self.stderr_steams.write("\t")
            self.stderr_steams.write(doc)
        self.stderr_steams.write("\n")

        GeneralLogger().get_logger().info("跳过测试：{}".format(test))
        self.result.append((3, test, HandlerFactory.get_stream_value(), ''))

    def startTest(self, test):
        # self.complete_std_in()
        GeneralLogger().get_logger(True)
        GeneralLogger().get_logger().info("开始测试：{}".format(test))
        TestResult.startTest(self, test)

    def stopTest(self, test):
        GeneralLogger().get_logger().info("测试结束：{}".format(test))
        HandlerFactory.get_stream_value()

    def addSuccess(self, test):
        self.success_count += 1
        TestResult.addSuccess(self, test)
        self.stdout_steams.write('Pass\t')
        self.stdout_steams.write(str(test))
        doc = test._testMethodDoc
        if doc:
            self.stdout_steams.write("\t")
            self.stdout_steams.write(doc)
        self.stdout_steams.write('\n')
        GeneralLogger().get_logger().info("测试执行通过：{}".format(test))
        self.result.append((0, test, HandlerFactory.get_stream_value(), ''))

    def addError(self, test, err):
        self.error_count += 1
        TestResult.addError(self, test, err)
        _, _exc_str = self.errors[-1]
        self.stderr_steams.write('Error\t')
        self.stderr_steams.write(str(test))
        doc = test._testMethodDoc
        if doc:
            self.stderr_steams.write("\t")
            self.stderr_steams.write(doc)
        self.stderr_steams.write('\n')
        GeneralLogger().get_logger().error("测试产生错误：\t{}".format(test))
        self.result.append((2, test, HandlerFactory.get_stream_value(), _exc_str))

    def addFailure(self, test, err):
        self.failure_count += 1
        TestResult.addFailure(self, test, err)
        _, _exc_str = self.failures[-1]
        self.stderr_steams.write('Fail\t')
        self.stderr_steams.write(str(test))
        doc = test._testMethodDoc
        if doc:
            self.stderr_steams.write("\t")
            self.stderr_steams.write(doc)
        self.stderr_steams.write('\n')
        GeneralLogger().get_logger().warning("测试未通过：{}".format(test))
        self.result.append((1, test, HandlerFactory.get_stream_value(), _exc_str))
