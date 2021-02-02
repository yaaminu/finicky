class Schema(object):
    def __init__(self, conf):
        self.conf = conf

    def validate(self, data):
        raise NotImplementedError
