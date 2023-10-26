from bson import ObjectId

from config import MAX_NOTIFICATIONS, EMAIL
from database import collection
from schemas import Notification
from utils import next_oid


def get_notes_count(user_id: str | ObjectId):
    user_id = str(user_id)
    count = collection.aggregate(
        [
            {
                '$match': {
                    '_id': ObjectId(user_id)
                }
            }, {
            '$project': {
                '_id': 0,
                'notifications': '$notifications.id'
            }
        }, {
            '$unwind': {
                'path': '$notifications'
            }
        }, {
            '$count': 'notifications'
        }
        ]
    )
    for i in count:
        return i['notifications']


def create_user(user_id: str | ObjectId):
    user_id = str(user_id)
    collection.insert_one({"_id": ObjectId(user_id), "email": EMAIL, "notifications": []})


def get_user(user_id: str | ObjectId):
    user_id = str(user_id)
    user = collection.find_one({"_id": ObjectId(user_id)})
    return user


def add_notification(note: Notification):
    user = get_user(note.user_id)
    note.id = ObjectId(next_oid(get_last_notification_id(note.user_id)))
    note.user_id = ObjectId(note.user_id)
    if note.target_id is not None:
        note.target_id = ObjectId(note.target_id)
    if user is not None:
        count = get_notes_count(note.user_id)
        print(count)
        if count >= MAX_NOTIFICATIONS:
            collection.update_one({"_id": ObjectId(note.user_id)},
                                  {"$pop": {"notifications": -1}})

        collection.update_one({"_id": ObjectId(note.user_id)},
                              {"$push": {"notifications": note.model_dump()}})
    else:
        create_user(note.user_id)
        collection.update_one({"_id": ObjectId(note.user_id)},
                              {"$push": {"notifications": note.model_dump()}})


def get_last_notification_id(user_id: str | ObjectId):
    user_id = str(user_id)
    last_id = collection.aggregate(
        [
            {
                '$match': {
                    '_id': ObjectId(user_id)
                }
            }, {
            '$project': {
                '_id': 0,
                'notifications.id': 1
            }
        }, {
            '$addFields': {
                'last_id': {
                    '$last': '$notifications.id'
                }
            }
        }, {
            '$project': {
                'notifications': 0
            }
        }
        ]
    )

    for i in last_id:
        print(i)
        if i is not None:
            return i['last_id']
    return ObjectId()


def get_notifications(user_id: str | ObjectId, skip: int, limit: int):
    user_id = str(user_id)
    notes = []
    for i in collection.aggregate(
        [
            {
                '$match': {
                    '_id': ObjectId(user_id)
                }
            }, {
            '$project': {
                '_id': 0,
                'notifications': 1
            }
        }, {
            '$unwind': {
                'path': '$notifications'
            }
        }, {
            '$project': {
                'id': '$notifications.id',
                'timestamp': '$notifications.timestamp',
                'key': '$notifications.key',
                'is_new': '$notifications.is_new',
                'user_id': '$notifications.user_id',
                'target_id': '$notifications.target_id',
                'data': '$notifications.data'
            }
        }, {
            '$skip': skip
        }, {
            '$limit': limit
        }
        ]
    ):
        i['id'] = str(i['id'])
        i['user_id'] = str(i['user_id'])
        i['target_id'] = str(i['target_id'])
        notes.append(i)
    print(notes)
    return notes


def update_note(user_id: str | ObjectId, note_id: str | ObjectId, **kwargs):
    note_id = str(note_id)
    user_id = str(user_id)
    opts = dict()
    for k, v in kwargs.items():
        opts[f"notifications.$.{k}"] = v
    collection.update_one(
        {
            "_id": ObjectId(user_id),
            "notifications": {"$elemMatch": {"id": ObjectId(note_id)}}
        },
        {"$set": opts}
    )
