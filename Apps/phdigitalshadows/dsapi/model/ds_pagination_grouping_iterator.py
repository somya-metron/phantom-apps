#
# Copyright (c) 2017 Digital Shadows Ltd.
#

from .ds_model import DSModel


class DSPaginationGroupingIterator(object):
    """
    Iterator that will Stream page groups of DSModel objects from the Provider.

    Provider *must* be a scrolling_request generator which yields a Digital Shadows page dictionary.
    Digital Shadows page dictionary:
    {
      'content': [],
      'currentPage: {
        'offset': int,
        'size': int
      },
      'total': int
    }
    """

    def __init__(self, provider, cls):
        """
        :type provider: generator
        :type cls: DSModel
        """
        self._provider = provider
        self._cls = cls

        self._page = self._provider.__next__()

    def current_page_offset(self):
        return int(self._page['current_page']['offset'])

    def current_page_size(self):
        return int(self._page['current_page']['size'])

    def __len__(self):
        return int(self._page['total'])

    def __iter__(self):
        return self

    def __next__(self):
        if self._page is None:
            self._page = self._provider.__next__()

        ds_model_group = []
        for ds_model_json in self._page['content']:
            ds_model_group.append(self._cls.from_json(ds_model_json))

        self._page = None
        return ds_model_group