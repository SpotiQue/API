import asyncio
import json
from ..models.track import Track
from sqlalchemy import Table, MetaData, Column, Integer, String, create_engine, Boolean
from sqlalchemy.orm import mapper, sessionmaker

metadata = MetaData()

mapper(
    Track,
    Table(
        'track',
        metadata,
        Column('id', Integer, primary_key=True),
        Column('title', String(255)),
        Column('artists', String(255)),
        Column('uri', String(255), unique=True),
        Column('skip_count', Integer),
        Column('is_queued', Boolean),
    )
)

engine = create_engine("postgres:///spotique")
Session = sessionmaker(bind=engine)

metadata.create_all(engine)


class QueueManager:
    _set_key = "queue"

    def __init__(self, queue_notifier, web_api):
        self.queue_notifier = queue_notifier
        self.web_api = web_api
        self.session = Session()

    def _track_to_redis(self, track):
        return json.dumps({
            "uri": track.uri,
            "artists": track.artists,
            "title": track.title,
        }, sort_keys=True)

    def _redis_to_track(self, track):
        return Track(**json.loads(track.decode()))

    @classmethod
    @asyncio.coroutine
    def create(cls, *args):
        manager = cls(*args)
        queue = yield from manager.get_queue()
        yield from manager.queue_notifier.notify(queue)
        return manager

    @asyncio.coroutine
    def get_queue(self):
        queue_members = self.session.query(Track).filter_by(is_queued=True).all()
        return sorted(queue_members, key=lambda x: x.title)

    def get_or_create_track(self, track):
        gotten_track = self.session.query(Track).filter_by(uri=track.uri).first()
        if gotten_track:
            return gotten_track
        else:
            self.session.add(track)
            return track

    @asyncio.coroutine
    def add_to_queue(self, track_uri):
        track = yield from self.web_api.get_track_info(track_uri)
        track = self.get_or_create_track(track)
        track.is_queued = True

        self.session.commit()

        queue = yield from self.get_queue()
        yield from self.queue_notifier.notify(queue)
        return track
