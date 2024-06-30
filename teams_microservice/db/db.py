import datetime
import json

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import insert, update, delete, and_, select, text

import models
from models import get_db

count = 1


async def get_users_for_team_db(team_id: int, db: Session):
    return (db.query(models.TeamMember)
            .filter(models.TeamMember.team_id == team_id)
            .all())


# TODO: ДОДЕЛАТЬ
async def get_teams_for_user_db(user_id: int, db: Session):
    # return (db.query(models.UsersTeams.team_id)
    #         # .join(models.Team, models.UsersTeams.team_id == models.Team.id)
    #         .filter(models.UsersTeams.user_id == user_id)
    #         .all())
    # db.execute(select(models.UsersTeams)
    #            .filter(models.UsersTeams.user_id == user_id))

    sql = f"""
        select * from team
        where id in (
        select team_id from users_teams
        where user_id = {user_id}
        )
    """

    result = db.execute(text(sql))
    # teams = result.fetchall()

    db.commit()
    # print(teams)
    return result


async def add_user_for_team_db(user_details, db: Session):
    db.execute(insert(models.UsersTeams)
               .values(user_id=user_details.id, team_id=user_details.team_id)
               )
    result = db.execute(insert(models.TeamMember)
                        .values(
        team_id=user_details.team_id,
        user_id=user_details.id,
        username=user_details.username,
        role="Участник",
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )
                        .returning(models.TeamMember))
    db.commit()
    return result.scalars().one()


async def delete_user_for_team_db(team_id: int, user_id: int, db: Session):
    db.execute(delete(models.UsersTeams)
               .filter(and_(models.UsersTeams.team_id == team_id,
                            models.UsersTeams.user_id == user_id))
               )
    db.execute(delete(models.TeamMember)
               .filter(models.TeamMember.user_id == user_id)
               )
    db.commit()


async def create_team_for_user_db(team, db: Session):
    global count
    result = db.execute(insert(models.Team)
                        .values(
        name=team.name,
        description=team.description,
        img_profile_ref=team.img_profile_ref,
        team_ref=str(count),
        user_creator_id=team.user_creator_id,
        owner_username=team.owner_username,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )
                        .returning(models.Team)
                        )
    db.flush()
    row = result.scalars().all()[0]
    db.execute(insert(models.UsersTeams)
               .values(user_id=team.user_creator_id,
                       team_id=row.id)
               )
    db.execute(insert(models.TeamMember)
               .values(team_id=row.id,
                       user_id=row.user_creator_id,
                       username=team.owner_username,
                       role="Владелец",
                       created_at=row.created_at,
                       updated_at=row.updated_at)
               )
    db.commit()
    count += 1
    return row


# TODO: ДОДЕЛАТЬ ИЗ-ЗА ОДИН-К-ОДНОМУ ПОСТ-КОНТЕНТ_ПОСТА
async def get_posts_for_team_db(team_id: int, db: Session):
    lst = []
    posts = db.execute(select(models.Post)
                        .filter(models.Post.team_id == team_id))
    db.flush()
    posts_appended = posts.scalars().all()
    for post in posts_appended:
        post_content = db.execute(select(models.PostContent)
                               .filter(models.PostContent.id == post.id))
        curr_post_content = post_content.scalars().all()[0]
        post_final = {
            'id': post.id,
            'team_id': post.team_id,
            'team_member_creator_id': post.team_member_creator_id,
            'team_member_creator_username': post.team_member_creator_username,
            # 'created_at': post.created_at,
            'text': curr_post_content.text,
            'img_ref': curr_post_content.img_ref,
            'file_ref': curr_post_content.file_ref,
            'audio_ref': curr_post_content.audio_ref,
            'video_ref': curr_post_content.video_ref,
        }
        lst.append(post_final)
    db.commit()
    return lst


async def apply_join_team_db(req, db: Session):
    result = db.execute(insert(models.PendingRequest)
                        .values(user_id=req.user_id,
                                username=req.username,
                                email=req.email,
                                team_id=req.team_id)
                        .returning(models.PendingRequest))
    db.commit()

    res = result.scalars().all()[0]
    print(res)
    return res


async def get_team_by_reference_db(req, db: Session):
    result = db.execute(select(models.Team)
                        .filter(models.Team.team_ref == str(req)))
    db.commit()
    # print(result.scalars().all())
    res = result.scalars().all()[0]
    print(res.id)
    # print(res[0])
    # print(res[0].name)
    return res


# TODO: ДОДЕЛАТЬ
async def create_post_for_team_db(post, db: Session):
    result_post = db.execute(insert(models.Post)
                             .values(
        team_id=post.team_id,
        team_member_creator_id=post.team_member_creator_id,
        team_member_creator_username=post.team_member_creator_username,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )
                             .returning(models.Post))
    result_post_content = db.execute(insert(models.PostContent)
                                     .values(
        text=post.text,
        img_ref=post.img_ref,
        file_ref=post.file_ref,
        audio_ref=post.audio_ref,
        video_ref=post.video_ref,
    )
                                     .returning(models.PostContent))
    db.flush()
    post_appended, post_content_appended = result_post.scalars().all()[0], result_post_content.scalars().all()[0]
    db.execute(insert(models.PostsContents)
    .values(
        post_id=post_appended.id,
        post_content_id=post_content_appended.id,
    ))
    db.commit()
    result = {'post_id': post_appended.id,
              'team_id': post_appended.team_id,
              'team_member_creator_id': post_appended.team_member_creator_id,
              'team_member_creator_username': post_appended.team_member_creator_username,
              # 'created_at': post_appended.created_at,
              'text': post_content_appended.text,
              'img_ref': post_content_appended.img_ref,
              'file_ref': post_content_appended.file_ref,
              'audio_ref': post_content_appended.audio_ref,
              'video_ref': post_content_appended.video_ref}
    return result


async def edit_post_for_team_db(post, db: Session):
    # post_content = db.execute(select(models.PostContent)
    #                           .filter(models.PostsContents.post_id == post.id)
    #                           )

    post_content = db.get(models.PostContent, post.post_id)
    if post.text is not None:
        post_content.text = post.text
    if post.img_ref is not None:
        post_content.img_ref = post.img_ref
    if post.file_ref is not None:
        post_content.file_ref = post.file_ref
    if post.audio_ref is not None:
        post_content.audio_ref = post.audio_ref
    if post.video_ref is not None:
        post_content.video_ref = post.video_ref
    db.add(post_content)
    db.commit()
    return post_content


async def delete_post_for_team_db(post_id: int, db: Session = Depends(get_db)):
    db.execute(delete(models.PostsContents)
               .filter(models.PostsContents.post_id == post_id))
    db.execute(delete(models.Post)
               .filter(models.Post.id == post_id))
    db.execute(delete(models.PostContent)
               .filter(models.PostContent.id == post_id))
    db.commit()


async def get_comments_for_post_db(team_id: int, post_id: int, db: Session = Depends(get_db)):
    pass


async def create_comment_for_post_db(comment, db: Session):
    result = db.execute(insert(models.PostComment)
                        .values(post_id=comment.post_id,
                                team_member_creator_id=comment.team_member_creator_id,
                                text=comment.text,
                                img_ref=comment.img_ref,
                                file_ref=comment.file_ref,
                                audio_ref=comment.audio_ref,
                                video_ref=comment.video_ref)
                        .returning(models.PostComment))

    db.flush()
    comment_appended = result.scalars().all()[0]

    db.execute(insert(models.PostRepliedComment)
               .values(comment_id=comment_appended.id,
                       parent_comment_id=comment.parent_comment_id))

    db.commit()

    return comment_appended


async def edit_comment_for_post_db(team_id: int, post_id: int, comment_id: int, db: Session = Depends(get_db)):
    pass


async def delete_comment_for_post_db(team_id: int, post_id: int, comment_id: int, db: Session = Depends(get_db)):
    pass


async def get_reference_for_team_db(team_id: int, db: Session = Depends(get_db)):
    pass


async def get_pending_requests_for_team_db(team_id: int, db: Session = Depends(get_db)):
    result = db.execute(select(models.PendingRequest)
                        .filter(models.PendingRequest.team_id == team_id))
    db.commit()

    return result


async def accept_pending_request_for_team_db(req, db: Session = Depends(get_db)):
    db.execute(insert(models.UsersTeams)
               .values(user_id=req.user_id,
                       team_id=req.team_id))
    result = db.execute(insert(models.TeamMember)
                        .values(user_id=req.user_id,
                                team_id=req.team_id,
                                username=req.username,
                                role="Участник")
                        .returning(models.TeamMember))
    db.execute(delete(models.PendingRequest)
    .filter(
        and_(models.PendingRequest.user_id == req.user_id, models.PendingRequest.team_id == req.team_id)))
    db.commit()
    return result.scalars().all()[0]


async def reject_pending_request_for_team_db(req, db: Session = Depends(get_db)):
    db.execute(delete(models.PendingRequest)
    .filter(
        and_(models.PendingRequest.user_id == req.user_id, models.PendingRequest.team_id == req.team_id)))
    db.commit()

    return 0


async def change_user_role_in_team_db(req, db: Session):
    result = db.execute(update(models.TeamMember)
                        .values(role=req.user_role)
                        .filter(
        and_(models.TeamMember.user_id == req.user_id, models.TeamMember.team_id == req.team_id))
                        .returning(models.TeamMember))
    db.commit()

    return result.scalars().all()[0]

