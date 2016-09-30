from __future__ import unicode_literals

import graphene
from graphql.execution.executors.gevent import GeventExecutor


# TODO(edit)
class Query():
    pass

# TODO(edit)
class Mutation():
    pass

# TODO(edit)
schema = graphene.Schema(name='xxxxxxxxxx')
schema.query = Query
schema.mutation = Mutation
schema.executor = GeventExecutor()
