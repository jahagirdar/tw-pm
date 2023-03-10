import datetime
import logging
from taskw import TaskWarrior
from fastapi import FastAPI, Body
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from typing import List
from pydantic import BaseModel
import json
logger = logging.getLogger("fastapi")
logger.setLevel(logging.INFO)
app = FastAPI()
app.mount("/front", StaticFiles(directory="front/public", html=True), name="front")
app.mount("/build", StaticFiles(directory="front/public/build"), name="build")


logger.info("Hello Logging")


@app.get('/')
async def front():
    return RedirectResponse(url='front')


@app.get("/tasks")
async def root():
    tw = TaskWarrior().load_tasks()
    dependuuid = []
    for t in tw['pending']:
        t['show'] = True
        if t.get('depends'):
            dependuuid.extend(t['depends'])
    for t in tw['pending']:
        if t['uuid'] in dependuuid:
            t['show'] = False
    return tw
    # return {"message": "Hello World"}


@app.get("/projects")
def projects():
    tw = TaskWarrior().load_tasks()
    lst = list(set([t.get('project') for t in tw['pending']]))
    return [{
        'project': p,
        'selected': False,
        'id': idx} for idx, p in enumerate(lst)]


class DoneReq(BaseModel):
    id: int
    uuid: str


class NewTask(BaseModel):
    description: str
    assign: str
    due: str
    project: str


class Annotation(BaseModel):
    entry: str
    description: str


class Task(BaseModel):
    uuid: str
    id: int
    assign: str = None
    description: str
    due: str = None
    effort: str = None
    entry: str
    modified: str
    project: str = None
    status: str = None
    tags: list[str] = None
    urgency: int = None
    annotations: list[Annotation] = None


class OneAnnotation(BaseModel):
    uuid: str
    annotation: str


@app.post("/saveTask")
def saveTask(task: Task):
    tw = TaskWarrior()
    id, t = tw.get_task(uuid=task.uuid)
    uuid: str
    if task.assign:
        t['assign'] = task.assign
    if task.description:
        t['description'] = task.description
    if task.due:
        t['due'] = datetime.datetime.strptime(task.due, "%Y-%m-%dT%H:%M")
    if task.project:
        t['project'] = task.project
    if task.status:
        t['status'] = task.status
    if task.tags:
        t['tags'] = task.tags
    if task.effort:
        t['effort'] = task.effort
    # if task.urgency:
    #     int = None
    # if task.annotations:
    #     list[Annotation] = None
    logger.info(f"Before update= {t}")
    tw.task_update(t)
    id, x = tw.get_task(uuid=task.uuid)
    logger.info(f"After update= {x}")
    return t


@app.post("/newTask")
def newTask(task: NewTask):
    tw = TaskWarrior(marshal=True)
    tw.task_add(description=task.description,
                assign=task.assign, project=task.project,
                due=datetime.datetime.strptime(task.due, "%Y-%m-%d")
                )
    print(task)
    return task
    # tw = TaskWarrior().get_task(id=req.id)
    # print(tw, req)
    # assert tw[1]['uuid'] == req.uuid, "Error Task UUID did not match"
    # TaskWarrior().task_done(id=req.id)


@app.post("/addAnnotate")
def add_annotation(ann: OneAnnotation = Body(
    example={'uuid': 'xxxx',
             'annotation': 'abd def'
             }
)):
    logger.info(ann)
    tw = TaskWarrior()
    id, t = tw.get_task(uuid=ann.uuid)
    if hasattr(t, 'annotations'):
        dt = datetime.datetime.now().replace(
            microsecond=0).isoformat().replace(":", '').replace("-", '')
        t['annotations'].append(
            {'entry': dt, 'description': ann.annotation})
    else:
        t['annotations'] = [ann.annotation]

    logger.info(f"Updating with{t}")
    tw.task_update(t)
    return t


@app.post("/done")
def done(req: DoneReq):
    tw = TaskWarrior().get_task(id=req.id)
    print(tw, req)
    assert tw[1]['uuid'] == req.uuid, "Error Task UUID did not match"
    TaskWarrior().task_done(id=req.id)
