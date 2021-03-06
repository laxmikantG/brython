from browser import ajax

from .futures import Future


class HTTPException(Exception):
    """
        A class representing a HTTPRequest error
    """
    def __init__(self, request):
        super(HTTPException, self).__init__()
        self.req = request


class HTTPRequest(Future):
    """
        A class representing a Future HTTPRequest result.
    """
    METHOD_POST = 'POST'
    METHOD_GET = 'GET'

    def __init__(self, url, method='GET', data=None, **kwargs):
        super(HTTPRequest, self).__init__(**kwargs)
        self._url = url
        self._req = ajax.ajax()
        self._req.bind("complete", self._complete_handler)
        self._data = data
        self._method = method
        self._req.open(self._method, self._url, True)
        self._req.set_header('content-type', 'application/x-www-form-urlencoded')
        if self._data is None:
            self._req.send()
        else:
            self._req.send(self._data)

    def cancel(self):
        self._req.abort()
        super().cancel()

    def _complete_handler(self, req):
        if req.status == 200 or req.status == 0:
            self.set_result(req)
        else:
            self.set_exception(HTTPException(req))
