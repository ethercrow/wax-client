

class GuiMessage(object):

    HIERARCHY = 0
    PROPERTY = 1

    def __init__(self, kind, payload):
        self.kind = kind
        self.payload = payload


class CommMessage(object):

    HIERARCHY = 0
    PROPERTY = 1

    def __init__(self, kind, payload):
        self.kind = kind
        self.payload = payload
