
class Link:
    def __init__(self, text, url=None):
        self._text = text
        self._url = url

    def getText(self):
        return self._text

    def getUrl(self):
        return self._url if self._url else "about:none"

    def isActive(self):
        return self._url is not None