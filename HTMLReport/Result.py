import logging
import sys
from unittest import TestResult


class Result(TestResult):
    """
    定义继承自 unittest.TestResult 的 类。
    这里重写了 unittest.TestResult 的多个方法，比如 startTest(self, test) 等等
    """

    def __init__(self, verbosity=2):
        TestResult.__init__(self)
        super().__init__(verbosity)
        # self.outputBuffer = io.StringIO()
        # self.stdout0 = None
        # self.stderr0 = None
        self.success_count = 0
        self.failure_count = 0
        self.skip_count = 0
        self.error_count = 0
        self.verbosity = verbosity
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
        self.result.append((3, test, "", ''))
        if self.verbosity > 1:
            sys.stderr.write('Skip\t')
            sys.stderr.write(str(test))

            doc = test._testMethodDoc
            if doc:
                sys.stderr.write("\t")
                sys.stderr.write(doc)
            sys.stderr.write("\n")
        else:
            sys.stderr.write('S\t')
        logging.info("跳过测试：{}".format(test))

    def startTest(self, test):
        # self.complete_std_in()
        logging.info("开始测试：{}".format(test))
        TestResult.startTest(self, test)

    def stopTest(self, test):
        logging.info("测试结束：{}".format(test))

    def addSuccess(self, test):
        self.success_count += 1
        TestResult.addSuccess(self, test)
        self.result.append((0, test, "", ''))
        if self.verbosity > 1:
            sys.stdout.write('Pass\t')
            sys.stdout.write(str(test))
            doc = test._testMethodDoc
            if doc:
                sys.stdout.write("\t")
                sys.stdout.write(doc)
            sys.stdout.write('\n')
        else:
            sys.stdout.write('P\t')
        logging.info("测试执行通过：{}".format(test))

    def addError(self, test, err):
        self.error_count += 1
        TestResult.addError(self, test, err)
        _, _exc_str = self.errors[-1]
        self.result.append((2, test, "", _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('Error\t')
            sys.stderr.write(str(test))
            doc = test._testMethodDoc
            if doc:
                sys.stderr.write("\t")
                sys.stderr.write(doc)
            sys.stderr.write('\n')
        else:
            sys.stderr.write('E\t')
        logging.info("测试产生错误：\t{}".format(test))

    def addFailure(self, test, err):
        self.failure_count += 1
        TestResult.addFailure(self, test, err)
        _, _exc_str = self.failures[-1]
        self.result.append((1, test, "", _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('Fail\t')
            sys.stderr.write(str(test))
            doc = test._testMethodDoc
            if doc:
                sys.stderr.write("\t")
                sys.stderr.write(doc)
            sys.stderr.write('\n')
        else:
            sys.stderr.write('F\t')
        logging.info("测试未通过：{}".format(test))
