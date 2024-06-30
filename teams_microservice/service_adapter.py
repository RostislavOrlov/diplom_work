from fastapi import Depends
from sqlalchemy.orm import Session

from app import TeamsMicroservice
from models import get_db
from services.service import get_users_for_team, reject_pending_request_for_team, accept_pending_request_for_team, \
    get_pending_requests_for_team, get_reference_for_team, delete_comment_for_post, edit_comment_for_post, \
    create_comment_for_post, get_comments_for_post, delete_post_for_team, edit_post_for_team, create_post_for_team, \
    get_posts_for_team, create_team_for_user, delete_user_for_team, add_user_for_team, get_teams_for_user, \
    apply_join_team, get_team_by_reference, change_user_role_in_team


async def get_users_for_team_adapter(app: TeamsMicroservice, team_id: int,
                                     db: Session = Depends(get_db)):
    return await get_users_for_team(app, team_id, db)


async def get_teams_for_user_adapter(app: TeamsMicroservice, user_id: int,
                                     db: Session = Depends(get_db)):
    return await get_teams_for_user(app, user_id, db)


async def add_user_for_team_adapter(app: TeamsMicroservice,
                                    user_details,
                                    db: Session = Depends(get_db)):
    return await add_user_for_team(app, user_details, db)


async def delete_user_for_team_adapter(app: TeamsMicroservice, team_id: int, user_id: int,
                                       db: Session = Depends(get_db)):
    return await delete_user_for_team(app, team_id, user_id, db)


async def create_team_for_user_adapter(app: TeamsMicroservice, team_details,
                                       db: Session):
    return await create_team_for_user(app, team_details, db)


async def get_posts_for_team_adapter(app: TeamsMicroservice, team_id: int,
                                     db: Session = Depends(get_db)):
    return await get_posts_for_team(app, team_id, db)


async def apply_join_team_adapter(app: TeamsMicroservice, req, db: Session):
    return await apply_join_team(app, req, db)


async def get_team_by_reference_adapter(app: TeamsMicroservice, req, db: Session):
    return await get_team_by_reference(app, req, db)


async def create_post_for_team_adapter(app: TeamsMicroservice, post, db: Session):
    return await create_post_for_team(app, post, db)


async def edit_post_for_team_adapter(app: TeamsMicroservice, post,
                                     db: Session):
    return await edit_post_for_team(app, post, db)


async def delete_post_for_team_adapter(app: TeamsMicroservice, post_id: int,
                                       db: Session = Depends(get_db)):
    return await delete_post_for_team(app, post_id, db)


async def get_comments_for_post_adapter(app: TeamsMicroservice, team_id: int, post_id: int,
                                        db: Session = Depends(get_db)):
    return await get_comments_for_post(app, team_id, post_id, db)


async def create_comment_for_post_adapter(app: TeamsMicroservice, comment,
                                          db: Session = Depends(get_db)):
    return await create_comment_for_post(app, comment, db)


async def edit_comment_for_post_adapter(app: TeamsMicroservice, team_id: int, post_id: int, comment_id: int,
                                        db: Session = Depends(get_db)):
    return await edit_comment_for_post(app, team_id, post_id, comment_id, db)


async def delete_comment_for_post_adapter(app: TeamsMicroservice, team_id: int, post_id: int, comment_id: int,
                                          db: Session = Depends(get_db)):
    return await delete_comment_for_post(app, team_id, post_id, comment_id, db)


async def get_reference_for_team_adapter(app: TeamsMicroservice, team_id: int,
                                         db: Session = Depends(get_db)):
    return await get_reference_for_team(app, team_id, db)


async def get_pending_requests_for_team_adapter(app: TeamsMicroservice, team_id: int,
                                                db: Session = Depends(get_db)):
    return await get_pending_requests_for_team(app, team_id, db)


async def accept_pending_request_for_team_adapter(app: TeamsMicroservice, req,
                                                  db: Session = Depends(get_db)):
    return await accept_pending_request_for_team(app, req, db)


async def reject_pending_request_for_team_adapter(app: TeamsMicroservice, req,
                                                  db: Session = Depends(get_db)):
    return await reject_pending_request_for_team(app, req, db)


async def change_user_role_in_team_adapter(app: TeamsMicroservice, req,
                                                  db: Session = Depends(get_db)):
    return await change_user_role_in_team(app, req, db)
