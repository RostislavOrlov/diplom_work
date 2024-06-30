import datetime
import json

from fastapi import Depends
from sqlalchemy.orm import Session

from app import TeamsMicroservice
from db.db import get_users_for_team_db, get_teams_for_user_db, add_user_for_team_db, \
    reject_pending_request_for_team_db, accept_pending_request_for_team_db, delete_comment_for_post_db, \
    edit_comment_for_post_db, create_comment_for_post_db, delete_post_for_team_db, edit_post_for_team_db, \
    create_post_for_team_db, create_team_for_user_db, delete_user_for_team_db, get_posts_for_team_db, \
    apply_join_team_db, get_team_by_reference_db, get_pending_requests_for_team_db, change_user_role_in_team_db
# from db_utils import get_db
import cache.cache
from models import get_db, Team
import pickle


async def get_users_for_team(app: TeamsMicroservice, team_id: int, db: Session = Depends(get_db)):
    app.logger.info("вызван метод get_users_for_team из сервисного слоя")
    # redis: Redis = await get_redis_connection()
    # кеширование и работа с базой данных
    # нужно будет вытащить еще и картинку профиля из микросервиса файлов
    # (gRPC запрос)
    cache_key = f'team_{team_id}_users'
    # result = await cache.cache.get_users_for_team_cache(app, cache_key)
    result = await get_users_for_team_db(team_id, db)
    # if not result:
    #     result = await get_users_for_team_db(team_id, db)
        # await app.redis.hset(cache_key, "user_ids", json.dumps(result))
    return result


async def get_teams_for_user(app: TeamsMicroservice, user_id: int, db: Session = Depends(get_db)):
    app.logger.info("вызван метод get_teams_for_user из сервисного слоя")
    return await get_teams_for_user_db(user_id, db)


async def add_user_for_team(app: TeamsMicroservice, user_details, db: Session):
    app.logger.info("вызван метод add_user_for_team из сервисного слоя")
    return await add_user_for_team_db(user_details, db)


async def delete_user_for_team(app: TeamsMicroservice, team_id: int, user_id: int, db: Session = Depends(get_db)):
    app.logger.info("вызван метод delete_user_for_team из сервисного слоя")
    return await delete_user_for_team_db(team_id, user_id, db)


async def create_team_for_user(app: TeamsMicroservice, team_details, db: Session):
    app.logger.info("вызван метод create_team_for_user из сервисного слоя")
    team = Team(
        name=team_details["name"],
        description=team_details["description"],
        img_profile_ref=team_details["img_profile_ref"],
        team_ref=team_details["name"],  # TODO: доделать team_ref
        user_creator_id=team_details["user_creator_id"],
        owner_username=team_details["owner_username"]
    )
    return await create_team_for_user_db(team, db)


async def get_posts_for_team(app: TeamsMicroservice, team_id: int, db: Session):
    app.logger.info("вызван метод get_posts_for_team из сервисного слоя")
    posts = await get_posts_for_team_db(team_id, db)
    return posts


async def apply_join_team(app: TeamsMicroservice, req, db: Session = Depends(get_db)):
    app.logger.info("вызван метод apply_join_team из сервисного слоя")
    result = await apply_join_team_db(req, db)
    return result


async def get_team_by_reference(app: TeamsMicroservice, req, db: Session = Depends(get_db)):
    app.logger.info("вызван метод get_team_by_reference из сервисного слоя")
    result = await get_team_by_reference_db(req, db)
    return result


async def create_post_for_team(app: TeamsMicroservice, post, db: Session):
    app.logger.info("вызван метод create_post_for_team из сервисного слоя")
    return await create_post_for_team_db(post, db)


async def edit_post_for_team(app: TeamsMicroservice, post, db: Session = Depends(get_db)):
    app.logger.info("вызван метод edit_post_for_team из сервисного слоя")
    return await edit_post_for_team_db(post, db)


async def delete_post_for_team(app: TeamsMicroservice, post_id: int, db: Session = Depends(get_db)):
    app.logger.info("вызван метод delete_post_for_team из сервисного слоя")
    return await delete_post_for_team_db(post_id, db)


async def get_comments_for_post(app: TeamsMicroservice, team_id: int, post_id: int, db: Session = Depends(get_db)):
    app.logger.info("вызван метод get_comments_for_post из сервисного слоя")


async def create_comment_for_post(app: TeamsMicroservice, comment, db: Session = Depends(get_db)):
    app.logger.info("вызван метод create_comment_for_post из сервисного слоя")
    return await create_comment_for_post_db(comment, db)


async def edit_comment_for_post(app: TeamsMicroservice, team_id: int, post_id: int, comment_id: int,
                                db: Session = Depends(get_db)):
    app.logger.info("вызван метод edit_comment_for_post из сервисного слоя")
    return await edit_comment_for_post_db(team_id, post_id, comment_id, db)


async def delete_comment_for_post(app: TeamsMicroservice, team_id: int, post_id: int, comment_id: int,
                                  db: Session = Depends(get_db)):
    app.logger.info("вызван метод delete_comment_for_post из сервисного слоя")
    return await delete_comment_for_post_db(team_id, post_id, comment_id, db)


async def get_reference_for_team(app: TeamsMicroservice, team_id: int, db: Session = Depends(get_db)):
    app.logger.info("вызван метод get_reference_for_team из сервисного слоя")


async def get_pending_requests_for_team(app: TeamsMicroservice, team_id: int, db: Session = Depends(get_db)):
    app.logger.info("вызван метод get_pending_requests_for_team из сервисного слоя")
    return await get_pending_requests_for_team_db(team_id, db)


async def accept_pending_request_for_team(app: TeamsMicroservice, req,
                                          db: Session = Depends(get_db)):
    app.logger.info("вызван метод accept_pending_request_for_team из сервисного слоя")
    return await accept_pending_request_for_team_db(req, db)


async def reject_pending_request_for_team(app: TeamsMicroservice, req,
                                          db: Session = Depends(get_db)):
    app.logger.info("вызван метод reject_pending_request_for_team из сервисного слоя")
    return await reject_pending_request_for_team_db(req, db)


async def change_user_role_in_team(app: TeamsMicroservice, req,
                                                  db: Session = Depends(get_db)):
    app.logger.info("вызван метод change_user_role_in_team из сервисного слоя")
    return await change_user_role_in_team_db(req, db)
