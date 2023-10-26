from fastapi import FastAPI, BackgroundTasks, Depends
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from schemas import CreateNote
from dependencies import new_post, new_login, registration, get_list, \
    read_note

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

enum_dict = {
    "registration": registration,
    "new_post": new_post,
    "new_message": new_post,
    "new_login": new_login
}


@app.post('/create', summary='Создать новое уведомление')
async def create(note: CreateNote, background_task: BackgroundTasks):
    await enum_dict[note.key](note, background_task)
    return JSONResponse({"success": True}, status_code=201)


@app.get('/list', summary='Получить список уведомлений пользователя')
async def to_list(data=Depends(get_list)):
    return JSONResponse({"success": True, "data": data}, status_code=200)


@app.post('/read', summary='Отметить уведомление как прочитанное')
async def read(res=Depends(read_note)):
    return JSONResponse({"success": True}, status_code=200)
