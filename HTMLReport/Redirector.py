class OutputRedirector(object):
    """
    将输出进行重定向
    """

    def __init__(self, fp):
        self.fp = fp

    def write(self, s):
        self.fp.write(s)
        self.flush()

    def writelines(self, lines):
        self.fp.writelines(lines)
        self.flush()

    def flush(self):
        self.fp.flush()
