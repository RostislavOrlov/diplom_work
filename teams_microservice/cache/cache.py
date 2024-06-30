from typing import Set

from app import TeamsMicroservice
from models import Team, Post, PendingRequest


async def get_users_for_team_cache(app: TeamsMicroservice, cache_key: str):
    return await app.redis.hget(cache_key, key="user_ids")


async def get_teams_for_user_cache(app: TeamsMicroservice, cache_key: str):
    return await app.redis.hget(cache_key, key="teams")


async def add_user_for_team_cache(app: TeamsMicroservice, user_id: int, cache_key: str):
    user_ids: Set[int] = Set[int](await app.redis.hget(cache_key, key="user_ids"))
    await app.redis.hset(name=cache_key, key="user_ids", value=user_ids.add(user_id))


async def delete_user_for_team_cache(app: TeamsMicroservice, user_id: int, cache_key: str):
    user_ids: Set[int] = Set[int](await app.redis.hget(cache_key, key="user_ids"))
    await app.redis.hset(name=cache_key, key="user_ids", value=user_ids.remove(user_id))


# пример транзакции в Redis
async def create_team_for_user_cache(app: TeamsMicroservice, team: Team, cache_key: str):
    teams: Set[dict] = Set[dict](await app.redis.hget(cache_key, key="teams"))
    async with app.redis.pipeline(transaction=True) as pipe:
        await pipe.hset(name=cache_key, key="teams", value=teams.add(team))
        await pipe.hset(name="all_teams", key=str(team.id), value=team)
        await pipe.execute()

    # aioredis.utils.Pipeline


async def get_posts_for_team_cache(app: TeamsMicroservice, team_id: int, cache_key: str):
    return await app.redis.hget(cache_key, key="posts")


async def create_post_for_team_cache(app: TeamsMicroservice, post: Post, cache_key: str):
    posts: Set[dict] = Set[dict](await app.redis.hget(cache_key, key="posts"))
    await app.redis.hset(name=cache_key, key="posts", value=posts.add(post))


async def edit_post_for_team_cache(app: TeamsMicroservice, post: Post, cache_key: str):
    await create_post_for_team_cache(post, cache_key)


async def delete_post_for_team_cache(app: TeamsMicroservice, post: Post, cache_key: str):
    posts: Set[dict] = Set[dict](await app.redis.hget(cache_key, key="posts"))
    await app.redis.hset(name=cache_key, key="posts", value=posts.remove(post))


async def get_pending_requests_for_team_cache(app: TeamsMicroservice, team_id: int, cache_key: str):
    return await app.redis.hget(cache_key, key="pending_requests")


async def accept_pending_request_for_team_cache(app: TeamsMicroservice,
                                                pending_request: PendingRequest, cache_key: str):
    pending_requests: Set[dict] = Set[dict](await app.redis.hget(cache_key, key="pending_requests"))
    await app.redis.hset(name=cache_key, key="pending_requests", value=pending_requests.add(pending_request))


async def reject_pending_request_for_team_cache(app: TeamsMicroservice,
                                                pending_request: PendingRequest, cache_key: str):
    pending_requests: Set[dict] = Set[dict](await app.redis.hget(cache_key, key="pending_requests"))
    await app.redis.hset(name=cache_key, key="pending_requests", value=pending_requests.remove(pending_request))


async def get_comments_for_post_cache(app: TeamsMicroservice, cache_key_team: str, cache_key_post: str):
    # redis: Redis = await get_redis_connection()
    # posts: Set[Post] = Set[Post](await redis.hget(cache_key_team, key="posts"))
    # comments: Set[dict] = Set[dict](await redis.hget(cache_key_post, key="comments"))
    # return comments
    pass


async def create_comment_for_post_cache(app: TeamsMicroservice, team_id: int, post_id: int):
    pass


async def edit_comment_for_post_cache(app: TeamsMicroservice, team_id: int, post_id: int, comment_id: int):
    pass


async def delete_comment_for_post_cache(app: TeamsMicroservice, team_id: int, post_id: int, comment_id: int):
    pass


async def get_reference_for_team_cache(app: TeamsMicroservice, team_id: int, cache_key: str):
    pass
