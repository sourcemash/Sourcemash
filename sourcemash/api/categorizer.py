from . import api
from flask.ext.restful import Resource, reqparse, marshal, fields

from urlparse import urlparse
from rq import Queue
from rq.job import Job
from worker import create_worker
from worker.scraper import categorize_article_by_url
from worker.categorize import Categorizer


REDIS_CONNECTION = create_worker()
categorizer = Categorizer()


class CategorizerAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('url', type=str, required=True)
        super(CategorizerAPI, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()

        # Scrape feed (but don't fail if redis-server is down)
        try:
            q = Queue('categorize', connection=REDIS_CONNECTION)
            job = q.enqueue_call(func=categorize_article_by_url,
                                 args=(args.url, categorizer,),
                                 timeout=600)
        except:
            return {'errors': {'url': 'Worker not running!'}}, 422

        return {'job_id': job.id}


class CategorizerResultsAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('job_id', type=str, required=True)
        super(CategorizerResultsAPI, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        job = Job.fetch(args.job_id, connection=REDIS_CONNECTION)

        if job.is_finished:
            return {'ready': True,
                    'categories': job.result}, 200
        else:
            return {'ready': False}, 202


api.add_resource(CategorizerAPI, '/categorizer', endpoint='categorizer')
api.add_resource(CategorizerResultsAPI, '/categorizer/results',
                 endpoint='categorizer_results')
