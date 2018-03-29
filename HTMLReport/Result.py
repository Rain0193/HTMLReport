import threading
from io import StringIO
from unittest import TestResult

from HTMLReport.images import SaveImages
from HTMLReport.log.HandlerFactory import HandlerFactory
from HTMLReport.log.Logger import GeneralLogger


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
        返回结果是一个4个属性的字典的列表
        (
          result_code (0: success; 1: fail; 2: error; 3: skip),
          testCase_object,
          test_output (byte string),
          image_paths list,
        )
        """
        self.result = []
        self.result_tmp = {}
        self.image_paths = {}

    def startTest(self, test):
        GeneralLogger().get_logger(True)
        GeneralLogger().get_logger().info("开始测试：{}".format(test))
        self.result_tmp[str(threading.current_thread().ident)] = {'result_code': 0,
                                                                  'testCase_object': test,
                                                                  'test_output': '',
                                                                  'image_paths': []
                                                                  }
        TestResult.startTest(self, test)

    def stopTest(self, test):
        GeneralLogger().get_logger().info("测试结束：{}".format(test))

        current_id = str(threading.current_thread().ident)
        if current_id in SaveImages.imageList:
            self.result_tmp[current_id]["image_paths"] = SaveImages.imageList.pop(current_id)
        self.result_tmp[current_id]['test_output'] = HandlerFactory.get_stream_value()
        self.result.append(self.result_tmp.pop(current_id))

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

        GeneralLogger().get_logger().info("跳过测试：\t{}\n{}".format(test, reason))

        current_id = str(threading.current_thread().ident)
        self.result_tmp[current_id]["result_code"] = 3

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

        current_id = str(threading.current_thread().ident)
        self.result_tmp[current_id]["result_code"] = 0

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
        GeneralLogger().get_logger().error("测试产生错误：\t{}\n{}".format(test, _exc_str))

        current_id = str(threading.current_thread().ident)
        self.result_tmp[current_id]["result_code"] = 2

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
        GeneralLogger().get_logger().warning("测试未通过：\t{}\n{}".format(test, _exc_str))

        current_id = str(threading.current_thread().ident)
        self.result_tmp[current_id]["result_code"] = 1
