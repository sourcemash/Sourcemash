from tests.factories import *

from sourcemash.models import Feed

class FeedFactory(SQLAlchemyModelFactory):
    FACTORY_FOR = Feed
    FACTORY_SESSION = db.session

    id = factory.Sequence(lambda n: n)
    title = factory.Sequence(lambda n: u'Feed %d' % n)
    url = factory.Sequence(lambda n: u'superfeed%d.com/rss' % n)
    last_updated = datetime.min

    @factory.post_generation
    def items(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for item in extracted:
                self.items.append(item)

class TechCrunchFeedFactory(FeedFactory):
    title = "TechCrunch"
    url = "http://feeds.feedburner.com/techcrunch/startups?format=xml"