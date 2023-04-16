import time
import re

from django.utils.deprecation import MiddlewareMixin
from pycallgraph import PyCallGraph, Config, GlobbingFilter
from pycallgraph.output import GraphvizOutput


class PycallgraphMiddleware(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        m = re.search(r'(?<=/).+?(?=/)', request.path_info)
        # path = [m[0], m[1]]
        # print(m[0])
        config = Config()
        config.trace_filter = GlobbingFilter(exclude=['pycallgraph.*'])
        # graphviz = GraphvizOutput(output_file='./callgraph/callgraph-' + str(time.time()) + '.png')
        graphviz = GraphvizOutput(output_file='./callgraph/callgraph-' + m[0] + str(time.time()) + '.png')
        pycallgraph = PyCallGraph(output=graphviz, config=config)
        pycallgraph.start()
        self.pycallgraph = pycallgraph

    def process_response(self, request, response):
        self.pycallgraph.done()
        return response
