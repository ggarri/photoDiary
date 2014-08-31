import simplejson


class MessageGlobal():
    _001 = "Incorrect request type"

    def __init__(self):
        pass


class MessageVO():
    def __init__(self, _type=False, msg=None, exception=None):
        self.type = _type
        if msg is not None:
            self.description = msg
        elif exception is not None:
            if exception.__class__ in dict.__subclasses__():
                self.description = exception

    def get_json(self):
        return simplejson.dumps({"type": self.type, "description": self.description })
