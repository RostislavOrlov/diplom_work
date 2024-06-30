from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean, Text, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

db_user = 'postgres'
db_password = '12345'
db_host = 'localhost'
db_port = '5433'
db_name = 'teams_microservice'

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:12345@localhost:5433/teams_microservice"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# уведомления канала?

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)


class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Team(Base):
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    img_profile_ref = Column(String, nullable=True)
    team_ref = Column(String)
    user_creator_id = Column(Integer)
    owner_username = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class TeamMember(Base):
    __tablename__ = 'team_member'

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey('team.id'))
    user_id = Column(Integer)
    username = Column(String)
    role = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey('team.id'))
    name = Column(String, index=True)
    description = Column(Text)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('project.id'))
    name = Column(String, index=True)
    description = Column(Text)
    author_id = Column(Integer)
    assignee_id = Column(Integer)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    state = Column(Text)
    # task_history_id = Column(Integer, ForeignKey(''))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    # tags = relationship('Tag', back_populates='task')


# class TaskHistory(Base):
#     __tablename__ = 'task_history'
#     id
#     task_id = OneToOne
#     prev_state
#     curr_state

class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # tasks = relationship('Task', back_populates='tag')


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey('team.id'))
    team_member_creator_id = Column(Integer)  # пусть будет user_id
    team_member_creator_username = Column(String)
    # content = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    # content = relationship()


class PostContent(Base):
    __tablename__ = 'post_content'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    img_ref = Column(String)
    file_ref = Column(String)
    audio_ref = Column(String)
    video_ref = Column(String)


class PostsContents(Base):
    __tablename__ = 'posts_contents'

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey('post.id'), unique=True)
    post_content_id = Column(Integer, ForeignKey('post_content.id'), unique=True)


class PostComment(Base):
    __tablename__ = 'post_comment'

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey('post.id'))
    team_member_creator_id = Column(Integer)
    text = Column(String)
    img_ref = Column(String)
    file_ref = Column(String)
    audio_ref = Column(String)
    video_ref = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class PostRepliedComment(Base):
    __tablename__ = 'post_replied_comment'

    id = Column(Integer, primary_key=True)
    comment_id = Column(Integer, ForeignKey('post_comment.id'))
    parent_comment_id = Column(Integer, ForeignKey('post_comment.id'))


class PendingRequest(Base):
    __tablename__ = 'pending_request'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    username = Column(String)
    email = Column(String)
    team_id = Column(Integer, ForeignKey('team.id'))


class UsersTeams(Base):
    __tablename__ = 'users_teams'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    team_id = Column(Integer, ForeignKey('team.id'))


class TasksTags(Base):
    __tablename__ = 'tasks_tags'

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey('task.id'))
    tag_id = Column(Integer, ForeignKey('tag.id'))


# Создание таблиц в базе данных
# Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
