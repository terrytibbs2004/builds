import re
import sys

try:
    from urllib.parse import parse_qs, urlparse
except ImportError:
    from urlparse import parse_qs, urlparse


class Rerouting:
    def __init__(self):
        (scheme, netloc, self._path, params, self._query, fragment) = urlparse(sys.argv[0] + sys.argv[2])
        self._baseurl = scheme + '://' + netloc
        self._handle = int(sys.argv[1])
        self._pathqs = (self._path + '?' + self._query) if self._query else self._path
        self._query = parse_qs(self._query)
        self._routemap = {}

    @property
    def handle(self):
        return self._handle

    @property
    def path(self):
        return self._path

    @property
    def pathqs(self):
        return self._pathqs

    @property
    def query(self):
        return self._query

    def route(self, pattern):
        """
        Registers a view function.

        :param pattern: A pattern to match.
        :return: A decorator.
        """

        def decorator(func):
            self._map_route(func, pattern)
            return func

        return decorator

    def run(self):
        """
        Executes the view function.

        :return: Returns True if a view function is found else None.
        """
        for (func, patterns) in self._routemap.items():
            for pattern in patterns:
                match = re.match('^{}$'.format(pattern), self._pathqs)

                if match is not None:
                    try:
                        func(**match.groupdict())
                        return True
                    except TypeError:
                        pass

        return False

    def url_for(self, pathquery):
        """
        Constructs a URL for the addon using the path and the query.

        :param pathquery: A path with query.
        """
        return self._baseurl + (pathquery if pathquery.startswith('/') else '/' + pathquery)

    def _map_route(self, func, pattern):
        """
        Binds a pattern to the function.

        :param func: The function.
        :param pattern: A pattern.
        """
        if func not in self._routemap:
            self._routemap[func] = []

        self._routemap[func].append(pattern)
