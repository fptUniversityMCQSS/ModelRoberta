class Question:
    def __init__(self, qn, content, options):
        self.qn = qn
        self.content = content
        self.options = options
        self.answer = None

    def create_response(self):
        return AnsweringResponse(self.qn, self.answer)


class Option:
    def __init__(self, key, content):
        self.key = key
        self.content = content


class AnsweringResponse:
    def __init__(self, qn, answer):
        self.qn = qn
        self.answer = answer