import datetime
import io
import os
import queue
import random
import sys
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from unittest import TestResult
from xml.sax import saxutils

from HTMLReport.Redirector import OutputRedirector
from HTMLReport.Template import TemplateMixin

__author__ = "刘士"
__version__ = "0.1.1"

# 日志输出
#   >>> logging.basicConfig(stream=HTMLReport.stdout_redirector)
#   >>> logging.basicConfig(stream=HTMLReport.stderr_redirector)

stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)


class _TestResult(TestResult):
    # 定义继承自 unittest.TestResult 的 类。
    # 这里重写了 unittest.TestResult 的多个方法，比如 startTest(self, test) 等等

    def __init__(self, verbosity=2):
        TestResult.__init__(self)
        super().__init__(verbosity)
        self.outputBuffer = io.BytesIO()
        self.stdout0 = None
        self.stderr0 = None
        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0
        self.verbosity = verbosity

        # 返回结果是一个4个属性的元组的列表
        # (
        #   result code (0: success; 1: fail; 2: error),
        #   TestCase object,
        #   Test output (byte string),
        #   stack trace,
        # )
        self.result = []

    def startTest(self, test):
        TestResult.startTest(self, test)
        # 仅为stdout和stderr提供一个缓冲区
        stdout_redirector.fp = self.outputBuffer
        stderr_redirector.fp = self.outputBuffer
        self.stdout0 = sys.stdout
        self.stderr0 = sys.stderr
        # sys.stdout = stdout_redirector
        # sys.stderr = stderr_redirector

    def complete_output(self):
        """
        断开输出重定向和返回缓冲区。
        可多次调用
        """
        if self.stdout0:
            sys.stdout = self.stdout0
            sys.stderr = self.stderr0
            self.stdout0 = None
            self.stderr0 = None
        return self.outputBuffer.getvalue()

    def stopTest(self, test):
        self.complete_output()

    def addSuccess(self, test):
        self.success_count += 1
        TestResult.addSuccess(self, test)
        output = self.complete_output()
        self.result.append((0, test, output, ''))
        if self.verbosity > 1:
            sys.stderr.write('ok ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('.')

    def addError(self, test, err):
        self.error_count += 1
        TestResult.addError(self, test, err)
        _, _exc_str = self.errors[-1]
        output = self.complete_output()
        self.result.append((2, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('E  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('E')

    def addFailure(self, test, err):
        self.failure_count += 1
        TestResult.addFailure(self, test, err)
        _, _exc_str = self.failures[-1]
        output = self.complete_output()
        self.result.append((1, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('F  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('F')


class TestRunner(TemplateMixin):
    """
    测试执行器
    """

    def __init__(self, report_file_name: str = 'test', output_path: str = None, title: str = None,
                 description: str = None, verbosity: int = 2, thread_count: int = 1,
                 sequential_execution: bool = False):
        self.output_path = output_path or "report"
        self.title = title or self.DEFAULT_TITLE
        self.description = description or self.DEFAULT_DESCRIPTION
        self.report_file_name = report_file_name
        self.verbosity = verbosity
        self.thread_count = thread_count
        self.sequential_execution = sequential_execution
        self.startTime = datetime.datetime.now()
        self.stopTime = datetime.datetime.now()

    def run(self, test):
        """
        运行给定的测试用例或测试套件。
        """
        result = _TestResult(self.verbosity)

        if self.sequential_execution:
            test_case_queue = queue.Queue()
            L = []
            tmp_key = None
            for test_case in test:
                tmp_class_name = test_case.__class__
                if tmp_key == tmp_class_name:
                    L.append(test_case)
                else:
                    tmp_key = tmp_class_name
                    if len(L) != 0:
                        test_case_queue.put(L.copy())
                        L.clear()
                    L.append(test_case)
            if len(L) != 0:
                test_case_queue.put(L.copy())
            while not test_case_queue.empty():
                tmp_list = test_case_queue.get()
                with ThreadPoolExecutor(self.thread_count) as pool:
                    for test_case in tmp_list:
                        pool.submit(test_case, result)
        else:
            with ThreadPoolExecutor(self.thread_count) as pool:
                for test_case in test:
                    pool.submit(test_case, result)

        self.stopTime = datetime.datetime.now()
        self.generateReport(result)
        print('\n运行时间: %s' % (self.stopTime - self.startTime), file=sys.stderr)
        return result

    @staticmethod
    def sortResult(result_list):
        # unittest似乎不以任何特定的顺序运行。
        # 在这里，至少我们想把它们按类分组。
        remap = {}
        classes = []
        for n, t, o, e in result_list:
            cls = t.__class__
            if cls not in remap:
                remap[cls] = []
                classes.append(cls)
            remap[cls].append((n, t, o, e))
        r = [(cls, remap[cls]) for cls in classes]
        return r

    def getReportAttributes(self, result):
        """
        返回报告属性作为一个列表 (name, value).
        覆盖这个以添加自定义属性。
        """
        startTime = str(self.startTime)[:19]
        duration = str(self.stopTime - self.startTime)
        status = []
        if result.success_count:
            status.append('Pass %s' % result.success_count)
        if result.failure_count:
            status.append('Failure %s' % result.failure_count)
        if result.error_count:
            status.append('Error %s' % result.error_count)
        if status:
            status = ' '.join(status)
        else:
            status = 'none'
        return [
            ('Start Time', startTime),
            ('Duration', duration),
            ('Status', status),
        ]

    def generateReport(self, result):
        report_attr = self.getReportAttributes(result)
        generator = 'HTMLReport %s' % __version__
        stylesheet = self._generate_stylesheet()
        heading = self._generate_heading(report_attr)
        report = self._generate_report(result)
        ending = self._generate_ending()
        output = self.HTML_TMPL % dict(
            title=saxutils.escape(self.title),
            generator=generator,
            stylesheet=stylesheet,
            heading=heading,
            report=report,
            ending=ending,
        )

        self.report_file_name = '{}_{}_{}.html'.format(self.report_file_name, time.strftime('%Y_%m_%d_%H_%M_%S'),
                                                       str(random.randint(1, 999)))
        current_dir = os.getcwd()
        dir_to = os.path.join(current_dir, self.output_path)
        if not os.path.exists(dir_to):
            os.makedirs(dir_to)
        path_file = os.path.join(dir_to, self.report_file_name)
        with open(path_file, 'wb') as report_file:
            report_file.write(output.encode('utf8'))

    def _generate_stylesheet(self):
        return self.STYLESHEET_TMPL

    def _generate_heading(self, report_attrs):
        a_lines = []
        for name, value in report_attrs:
            line = self.HEADING_ATTRIBUTE_TMPL % dict(
                name=saxutils.escape(name),
                value=saxutils.escape(value),
            )
            a_lines.append(line)
        heading = self.HEADING_TMPL % dict(
            title=saxutils.escape(self.title),
            parameters=''.join(a_lines),
            description=saxutils.escape(self.description),
        )
        return heading

    def _generate_report(self, result):
        rows = []
        sortedResult = self.sortResult(result.result)
        for cid, (cls, cls_results) in enumerate(sortedResult):
            np = nf = ne = 0
            for n, t, o, e in cls_results:
                if n == 0:
                    np += 1
                elif n == 1:
                    nf += 1
                else:
                    ne += 1

            # format class description
            if cls.__module__ == "__main__":
                name = cls.__name__
            else:
                name = "%s.%s" % (cls.__module__, cls.__name__)
            doc = cls.__doc__ and cls.__doc__.split("\n")[0] or ""
            desc = doc and '%s: %s' % (name, doc) or name

            row = self.REPORT_CLASS_TMPL % dict(
                style=ne > 0 and 'errorClass' or nf > 0 and 'failClass' or 'passClass',
                desc=desc,
                count=np + nf + ne,
                Pass=np,
                fail=nf,
                error=ne,
                cid='c%s' % (cid + 1),
            )
            rows.append(row)

            for tid, (n, t, o, e) in enumerate(cls_results):
                self._generate_report_test(rows, cid, tid, n, t, o, e)

        report = self.REPORT_TMPL % dict(
            test_list=''.join(rows),
            count=str(result.success_count + result.failure_count + result.error_count),
            Pass=str(result.success_count),
            fail=str(result.failure_count),
            error=str(result.error_count),
        )
        return report

    def _generate_report_test(self, rows, cid, tid, n, t, o, e):
        # e.g. 'pt1.1', 'ft1.1', etc
        has_output = bool(o or e)
        tid = (n == 0 and 'p' or 'f') + 't%s.%s' % (cid + 1, tid + 1)
        name = t.id().split('.')[-1]
        doc = t.shortDescription() or ""
        desc = doc and ('%s: %s' % (name, doc)) or name
        tmpl = has_output and self.REPORT_TEST_WITH_OUTPUT_TMPL or self.REPORT_TEST_NO_OUTPUT_TMPL

        script = self.REPORT_TEST_OUTPUT_TMPL % dict(
            id=tid,
            output=saxutils.escape(o.decode('utf-8') + e),
        )

        row = tmpl % dict(
            tid=tid,
            Class=(n == 0 and 'hiddenRow' or 'none'),
            style=n == 2 and 'errorCase' or (n == 1 and 'failCase' or 'none'),
            desc=desc,
            script=script,
            status=self.STATUS[n],
        )
        rows.append(row)
        if not has_output:
            return

    def _generate_ending(self):
        return self.ENDING_TMPL


class TestProgram(unittest.TestProgram):
    # 这里继承自 unittest.TestProgram 类，重写了 runTests 方法。
    # 用于命令行执行测试
    def runTests(self):
        if self.testRunner is None:
            self.testRunner = TestRunner(verbosity=self.verbosity)
        unittest.TestProgram.runTests(self)


if __name__ == "__main__":
    TestProgram(module=None)
