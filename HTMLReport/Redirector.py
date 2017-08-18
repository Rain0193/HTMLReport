class OutputRedirector(object):
    """
    将输出进行重定向
    """

    def __init__(self, fp):
        self.fp = fp

    def write(self, s):
        if type('') == type(s):
            self.fp.write(s.encode('utf-8'))
        else:
            self.fp.write(s)

    def writelines(self, lines):
        self.fp.writelines(lines)

    def flush(self):
        self.fp.flush()
