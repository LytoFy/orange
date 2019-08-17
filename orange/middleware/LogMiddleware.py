import logging

from django.utils.deprecation import MiddlewareMixin

err_log = logging.getLogger('err')


class ErrorMiddleware(MiddlewareMixin):

    def process_exception(self, request, exceptions):
        err_log.error(exceptions)
