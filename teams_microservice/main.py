import datetime
import json
import logging
from time import sleep
from typing import List

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

from app import TeamsMicroservice
from schemas import CreateTeamForUserRequest, CreateTeamForUserResponse, GetUsersForTeamResponse, TeamMemberDTO, \
    AddUserForTeamRequest, AddUserForTeamResponse, CreatePostForTeamRequest, CreatePostForTeamResponse, \
    EditPostForTeamResponse, EditPostForTeamRequest, CreateCommentForPostRequest, CreateCommentForPostResponse, \
    GetTeamsForUser, ApplyJoinTeamRequest, ApplyJoinTeamResponse, GetTeamByReferenceResponse, \
    GetPendingRequestsForTeamResponse, AcceptPendingRequestForTeamResponse, RejectPendingRequestForTeamRequest, \
    AcceptPendingRequestForTeamRequest, ChangeUserRoleInTeamRequest, ChangeUserRoleInTeamResponse, \
    GetPostsForTeamResponse
from models import get_db, engine, Base
import service_adapter
import pika

from validation import TeamDTO

app_fastapi = FastAPI()
app = TeamsMicroservice(app_fastapi)

origins = [
    "http://localhost:8080",
    # "ws://localhost:8080",
    "http://192.168.1.123:8080/",
    "http://192.168.1.123:8080",
    "http://192.168.1.179"
]

app_fastapi.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app_fastapi.on_event("startup")
async def startup_event():
    logging.basicConfig(filename='app.log', level=logging.INFO,
                        format='%(asctime)s | %(levelname)s | %(module)s | %(message)s')
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # channel = app.rabbitmq.channel()
    #
    # channel.queue_declare(queue='posts')
    # channel.basic_publish(exchange='',
    #                       routing_key='hello',
    #                       body='Hello World!'.encode())
    # print("Успешно?")


@app.app_fastapi.get("/teams/{team_id}/users")
async def get_users_for_team(team_id: int, db: Session = Depends(get_db)):
    app.logger.info("вызван метод get_users_for_team из слоя обработчиков")
    users = await service_adapter.get_users_for_team_adapter(app, team_id, db)
    usersDTO = list()
    for user in users:
        userDTO = TeamMemberDTO(
            id=user.id,
            team_id=user.team_id,
            user_id=user.user_id,
            username=user.username,
            role=user.role,
        )
        usersDTO.append(userDTO)
    response = GetUsersForTeamResponse(users=usersDTO)
    return {'result': response.model_dump()}
    # return {"status": "OK"}


@app.app_fastapi.get("/teams/{user_id}")
async def get_teams_for_user(user_id: int, db: Session = Depends(get_db)):
    app.logger.info("вызван метод get_teams_for_user из слоя обработчиков")
    result = await service_adapter.get_teams_for_user_adapter(app, user_id, db)
    lst = []
    for row in result.fetchall():
        curr_team = {'id': row[0], 'name': row[1], 'description': row[2], 'img_profile_ref': row[3], 'team_ref': row[4],
                     'user_creator_id': row[5], 'owner_username': row[6], 'created_at': row[7], 'updated_at': row[8]}
        lst.append(curr_team)

    resp = GetTeamsForUser(teams=lst)

    print("RESP", resp)
    return {'result': resp.model_dump_json()}


@app.app_fastapi.post("/teams/{team_id}/users/{user_id}")
async def add_user_for_team(user_details: AddUserForTeamRequest, db: Session = Depends(get_db)):
    app.logger.info("вызван метод add_user_for_team из слоя обработчиков")
    result = await service_adapter.add_user_for_team_adapter(app, user_details, db)
    response = AddUserForTeamResponse(
        id=result.user_id,
        username=result.username,
        team_id=result.team_id,
    )
    return {'result': response.model_dump()}


@app.app_fastapi.delete("/teams/{team_id}/users/{user_id}")
async def delete_user_for_team(team_id: int, user_id: int, db: Session = Depends(get_db)):
    app.logger.info("вызван метод delete_user_for_team из слоя обработчиков")
    await service_adapter.delete_user_for_team(app, team_id, user_id, db)
    return {'success': 'true'}


@app.app_fastapi.post("/teams/users/{user_id}")
async def create_team_for_user(user_id: int, body: CreateTeamForUserRequest,
                               db: Session = Depends(get_db)):
    app.logger.info("вызван метод create_team_for_user из слоя обработчиков")
    team_details = body.model_dump()
    team_details["user_creator_id"] = user_id
    result = await service_adapter.create_team_for_user_adapter(app, team_details, db)
    response = CreateTeamForUserResponse(
        team_id=result.id,
        name=result.name,
        description=result.description,
        img_profile_ref=result.img_profile_ref,
        team_ref=result.team_ref,
        user_creator_id=result.user_creator_id,
        owner_username=result.owner_username
    )
    return {'result': response.model_dump_json()}


class WebSocketConnectionManager:
    def __init__(self):
        # self.active_connections: List[WebSocket] = []
        self.active_connections = []

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections.append({'ws_connection': websocket, 'user_id': user_id})

    def get_ws_by_user_id(self, user_id) -> WebSocket:
        result_client = next(client for client in self.active_connections if client['user_id'] == user_id)
        return result_client['ws_connection']

    async def send_message(self, message, websocket: WebSocket):
        await websocket.send_text(message)

    async def process_message(self, payload, websocket: WebSocket, db: Session):
        if payload['request'] == 'getPostsForTeam':
            team_id = payload['params']['team_id']
            posts = await get_posts_for_team(team_id, db)
            # for client in self.active_connections:
            #     if client['id'] in user_ids:
            #         client['ws_connection'].send
            await websocket.send_json(posts)

        elif payload['request'] == 'createPostForTeam':
            req = CreatePostForTeamRequest(
                team_id=payload['params']['team_id'],
                team_member_creator_id=payload['params']['team_member_creator_id'],
                team_member_creator_username=payload['params']['team_member_creator_username'],
                text=payload['params']['text'],
                img_ref=payload['params']['img_ref'],
                file_ref=payload['params']['file_ref'],
                audio_ref=payload['params']['audio_ref'],
                video_ref=payload['params']['video_ref'],
            )
            resp = await create_post_for_team(req, db)
            await websocket.send_json(resp)

        elif payload['request'] == 'editPostForTeam':
            req = EditPostForTeamRequest(
                post_id=payload['params']['post_id'],
                text=payload['params']['text'],
                img_ref=payload['params']['img_ref'],
                file_ref=payload['params']['file_ref'],
                audio_ref=payload['params']['audio_ref'],
                video_ref=payload['params']['video_ref'],
            )
            resp = await edit_post_for_team(req, db)
            await websocket.send_json(resp)
            await get_users_for_team(req.team_id)

        elif payload['request'] == 'deletePostForTeam':
            req = payload['params']['post_id']
            resp = await delete_post_for_team(req, db)
            await websocket.send_json(resp)

        elif payload['request'] == 'getTeamByReference':
            req = payload['params']['team_code']
            resp = await get_team_by_reference(req, db)
            await websocket.send_json(resp)

        elif payload['request'] == 'applyJoinTeam':
            req = ApplyJoinTeamRequest(
                user_id=payload['params']['user_id'],
                username=payload['params']['username'],
                email=payload['params']['email'],
                team_id=payload['params']['team_id'],
            )
            resp = await apply_join_team(req, db)
            await websocket.send_json(resp)
            # second_websocket = await self.get_ws_by_user_id(req.user_id)
            resp = await get_users_for_team(req.team_id, db)
            for usr in resp['result']['users']:
                ws = self.get_ws_by_user_id(usr['user_id'])
                await ws.send_json(resp)

        elif payload['request'] == 'getPendingRequestsForTeam':
            req = payload['params']['team_id']
            resp = await get_pending_requests_for_team(req, db)
            await websocket.send_json(resp)

        elif payload['request'] == 'acceptPendingRequestForTeam':
            req = AcceptPendingRequestForTeamRequest(
                user_id=payload['params']['user_id'],
                team_id=payload['params']['team_id'],
                username=payload['params']['username'],
            )
            resp = await accept_pending_request_for_team(req, db)
            await websocket.send_json(resp)
            second_websocket = self.get_ws_by_user_id(req.user_id)
            await second_websocket.send_json(resp)

        elif payload['request'] == 'rejectPendingRequestForTeam':
            req = RejectPendingRequestForTeamRequest(
                user_id=payload['params']['user_id'],
                team_id=payload['params']['team_id'],
            )
            resp = await reject_pending_request_for_team(req, db)
            await websocket.send_json(resp)
            second_websocket = self.get_ws_by_user_id(req.user_id)
            await second_websocket.send_json(resp)

        elif payload['request'] == 'changeUserRoleInTeam':
            req = ChangeUserRoleInTeamRequest(
                user_id=payload['params']['user_id'],
                user_role=payload['params']['role'],
                team_id=payload['params']['team_id']
            )
            resp = await change_user_role_in_team(req, db)
            await websocket.send_json(resp)

    def disconnect(self, websocket: WebSocket):
        for connection in self.active_connections:
            if websocket == connection['ws_connection']:
                self.active_connections.remove(connection)


async def change_user_role_in_team(req: ChangeUserRoleInTeamRequest, db: Session = Depends(get_db)):
    app.logger.info("вызван метод change_user_role_in_team из слоя обработчиков")
    result = await service_adapter.change_user_role_in_team_adapter(app, req, db)
    response = ChangeUserRoleInTeamResponse(
        user_id=result.user_id,
        role=result.role,
        team_id=result.team_id
    )
    return {'request': 'changeUserRoleInTeam', 'params': response.model_dump()}


async def get_team_by_reference(req, db: Session = Depends(get_db)):
    app.logger.info("вызван метод get_team_by_reference из слоя обработчиков")
    result = await service_adapter.get_team_by_reference_adapter(app, req, db)
    response = GetTeamByReferenceResponse(
        id=result.id,
        name=result.name,
        description=result.description,
        img_profile_ref=result.img_profile_ref,
        team_ref=result.team_ref,
        user_creator_id=result.user_creator_id,
    )
    return {'request': 'getTeamByReference', 'params': response.model_dump()}


async def apply_join_team(req: ApplyJoinTeamRequest, db: Session = Depends(get_db)):
    app.logger.info("вызван метод apply_join_team из слоя обработчиков")
    result = await service_adapter.apply_join_team_adapter(app, req, db)
    response = ApplyJoinTeamResponse(
        id=result.id,
        user_id=result.user_id,
        username=result.username,
        email=result.email,
        team_id=result.team_id,
    )
    return {'request': 'applyJoinTeam', 'params': response.model_dump()}


# @app.app_fastapi.post("/teams/{team_id}/posts")
async def create_post_for_team(post: CreatePostForTeamRequest, db: Session = Depends(get_db)):
    app.logger.info("вызван метод create_post_for_team из слоя обработчиков")
    result = await service_adapter.create_post_for_team_adapter(app, post, db)
    response = CreatePostForTeamResponse(
        post_id=result['post_id'],
        team_id=result['team_id'],
        team_member_creator_id=result['team_member_creator_id'],
        team_member_creator_username=result['team_member_creator_username'],
        # created_at=json.dumps(result['created_at']),
        text=result['text'],
        img_ref=result['img_ref'],
        file_ref=result['file_ref'],
        audio_ref=result['audio_ref'],
        video_ref=result['video_ref'],
    )
    return {'request': 'createPostForTeam', 'params': response.model_dump()}


manager = WebSocketConnectionManager()


@app.app_fastapi.websocket("/ws/teams/{user_id}")
async def websocket_endpoint(user_id: int, websocket: WebSocket, db: Session = Depends(get_db)):
    # user_id = 2
    await manager.connect(websocket, user_id)
    # sleep(2)
    # await websocket.send_text('test')
    try:
        while True:
            # print(client_id)
            data = await websocket.receive_json()
            # db = get_db()
            await manager.process_message(data['payload'], websocket, db)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


async def get_posts_for_team(team_id, db: Session):
    app.logger.info("вызван метод edit_post_for_team из слоя обработчиков")
    result = await service_adapter.get_posts_for_team(app, team_id, db)
    lst = []
    for row in result:
        curr_post = {
            'post_id': row['id'],
            'team_id': row['team_id'],
            'team_member_creator_id': row['team_member_creator_id'],
            'team_member_creator_username': row['team_member_creator_username'],
            'text': row['text'],
            'img_ref': row['img_ref'],
            'file_ref': row['file_ref'],
            'audio_ref': row['audio_ref'],
            'video_ref': row['video_ref'],
        }
        lst.append(curr_post)

    response = GetPostsForTeamResponse(posts=lst)
    return {'request': 'getPostsForTeam', 'params': response.model_dump()}


async def edit_post_for_team(post: EditPostForTeamRequest, db: Session = Depends(get_db)):
    app.logger.info("вызван метод edit_post_for_team из слоя обработчиков")
    new_post = await service_adapter.edit_post_for_team_adapter(app, post, db)
    response = EditPostForTeamResponse(
        post_id=new_post.id,
        text=new_post.text,
        img_ref=new_post.img_ref,
        file_ref=new_post.file_ref,
        audio_ref=new_post.audio_ref,
        video_ref=new_post.video_ref,
    )
    return {'request': 'editPostForTeam', 'params': response.model_dump()}


# @app.app_fastapi.delete("/teams/{team_id}/posts/{post_id}")
async def delete_post_for_team(post_id: int, db: Session = Depends(get_db)):
    app.logger.info("вызван метод delete_post_for_team из слоя обработчиков")
    await service_adapter.delete_post_for_team_adapter(app, post_id, db)
    return {'request': 'deletePostForTeam', 'params': {'post_id': post_id}}


@app.app_fastapi.get("teams/{team_id}/posts/{post_id}")
async def get_comments_for_post(team_id: int, post_id: int):
    app.logger.info("вызван метод get_comments_for_post из слоя обработчиков")
    pass


@app.app_fastapi.post("/teams/{team_id}/posts/{post_id}/comments")
async def create_comment_for_post(post_comment: CreateCommentForPostRequest, db: Session = Depends(get_db)):
    app.logger.info("вызван метод create_comment_for_post из слоя обработчиков")
    result = await service_adapter.create_comment_for_post_adapter(app, post_comment, db)
    response = CreateCommentForPostResponse(
        comment_id=result.id,
        post_id=result.id,
        team_member_creator_id=result.team_member_creator_id,
        text=result.text,
        img_ref=result.img_ref,
        file_ref=result.file_ref,
        audio_ref=result.audio_ref,
        video_ref=result.video_ref,
    )
    return {'result': response}


@app.app_fastapi.patch("/teams/{team_id}/posts/{post_id}/comments/{comment_id}")
async def edit_comment_for_post(team_id: int, post_id: int, comment_id: int):
    app.logger.info("вызван метод edit_comment_for_post из слоя обработчиков")
    pass


@app.app_fastapi.delete("/teams/{team_id}/posts/{post_id}/comments/{comment_id}")
async def delete_comment_for_post(team_id: int, post_id: int, comment_id: int):
    app.logger.info("вызван метод delete_comment_for_post из слоя обработчиков")
    pass


#
# @app.app_fastapi.get("/teams/{team_id}/reference")
# async def get_reference_for_team(team_id: int):
#     app.logger.info("вызван метод get_reference_for_team из слоя обработчиков")
#     pass


# @app.app_fastapi.get("/teams/{team_id}/pending_requests")
async def get_pending_requests_for_team(team_id: int, db: Session):
    app.logger.info("вызван метод get_pending_requests_for_team из слоя обработчиков")
    result = await service_adapter.get_pending_requests_for_team_adapter(app, team_id, db)
    lst = []
    lst2 = result.scalars().all()
    for row in lst2:
        curr_user = {'user_id': row.user_id,
                     'username': row.username,
                     'email': row.email}
        lst.append(curr_user)

    response = GetPendingRequestsForTeamResponse(requests=lst)
    return {'request': 'getPendingRequestsForTeam', 'params': response.model_dump()}


# @app.app_fastapi.post("/teams/{team_id}/pending_requests/{pending_request_id}")
async def accept_pending_request_for_team(req: AcceptPendingRequestForTeamRequest, db: Session):
    app.logger.info("вызван метод accept_pending_request_for_team из слоя обработчиков")
    result = await service_adapter.accept_pending_request_for_team_adapter(app, req, db)
    response = AcceptPendingRequestForTeamResponse(
        id=result['id'],
        team_id=result['team_id'],
        user_id=result['user_id'],
        username=result['username'],
        role=result['role'],
    )
    return {'request': 'acceptPendingRequestForTeam', 'params': response.model_dump()}


# @app.app_fastapi.post("/teams/{team_id}/pending_requests/{pending_request_id}")
async def reject_pending_request_for_team(req: RejectPendingRequestForTeamRequest, db: Session):
    app.logger.info("вызван метод reject_pending_request_for_team из слоя обработчиков")
    await service_adapter.reject_pending_request_for_team_adapter(app, req, db)
    return {'request': 'rejectPendingRequestForTeam'}


# @app.websocket("/ws/teams/")
# async

@app.app_fastapi.on_event("shutdown")
async def shutdown_event():
    await app.redis.close()
    # app.rabbitmq.close()
