from fastapi import BackgroundTasks

from crud import add_notification, get_user, create_user, get_notifications, update_note
from schemas import CreateNote, Notification
from utils import send_email


async def read_note(user_id: str, notification_id: str):
    update_note(user_id, notification_id, is_new=False)
    return None


async def get_list(user_id: str, skip: int, limit: int):
    notes = get_notifications(user_id, skip, limit)
    count = 0
    for note in notes:
        if note['is_new']:
            count += 1
    result = {
        "elements": len(notes),
        "new": count,
        "request": {
            "user_id": user_id,
            "skip": skip,
            "limit": limit,
        },
        "list": notes
    }
    return result


async def registration(note: CreateNote, background_task: BackgroundTasks):
    print('registration')
    user = get_user(note.user_id)
    if user is not None:
        note = Notification.model_validate(note, from_attributes=True)
        background_task.add_task(send_email, email=user['email'], msg=note.key)
    else:
        create_user(note.user_id)
        user = get_user(note.user_id)
        background_task.add_task(send_email, email=user['email'], msg=note.key)


async def new_post(note: CreateNote, background_task: BackgroundTasks):
    print('new post')
    note = Notification.model_validate(note, from_attributes=True)
    add_notification(note)


async def new_login(note: CreateNote, background_task: BackgroundTasks):
    print('new login')
    note = Notification.model_validate(note, from_attributes=True)
    add_notification(note)
    user = get_user(note.user_id)
    background_task.add_task(send_email, email=user['email'], msg=note.key)


