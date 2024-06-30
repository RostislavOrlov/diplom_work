import datetime
from typing import Union, List, Optional

from pydantic import BaseModel

from validation import TeamDTO


class CreateTeamForUserRequest(BaseModel):
    name: str
    description: Union[str, None]
    img_profile_ref: Union[str, None]
    owner_username: str


class CreateTeamForUserResponse(BaseModel):
    team_id: int
    name: str
    description: Union[str, None]
    img_profile_ref: Union[str, None]
    team_ref: str
    user_creator_id: int
    owner_username: str


class TeamMemberDTO(BaseModel):
    id: int
    team_id: int
    user_id: int
    username: str
    role: str


class GetTeamsForUser(BaseModel):
    teams: List[TeamDTO]


class GetUsersForTeamResponse(BaseModel):
    users: List[TeamMemberDTO]
    # pass


class AddUserForTeamRequest(BaseModel):
    id: int
    username: str
    team_id: int


class AddUserForTeamResponse(BaseModel):
    id: int
    username: str
    team_id: int


class CreatePostForTeamRequest(BaseModel):
    team_id: int
    team_member_creator_id: int
    team_member_creator_username: str
    text: Optional[str] = None
    img_ref: Optional[str] = None
    file_ref: Optional[str] = None
    audio_ref: Optional[str] = None
    video_ref: Optional[str] = None


class CreatePostForTeamResponse(BaseModel):
    post_id: int
    team_id: int
    team_member_creator_id: int
    team_member_creator_username: str
    # created_at: datetime.datetime
    text: Optional[str] = None
    img_ref: Optional[str] = None
    file_ref: Optional[str] = None
    audio_ref: Optional[str] = None
    video_ref: Optional[str] = None


class EditPostForTeamRequest(BaseModel):
    post_id: int
    text: Optional[str] = None
    img_ref: Optional[str] = None
    file_ref: Optional[str] = None
    audio_ref: Optional[str] = None
    video_ref: Optional[str] = None


class EditPostForTeamResponse(BaseModel):
    post_id: int
    text: Optional[str] = None
    img_ref: Optional[str] = None
    file_ref: Optional[str] = None
    audio_ref: Optional[str] = None
    video_ref: Optional[str] = None


class CreateCommentForPostRequest(BaseModel):
    post_id: int
    team_member_creator_id: int
    parent_comment_id: Optional[int] = None
    text: Optional[str] = None
    img_ref: Optional[str] = None
    file_ref: Optional[str] = None
    audio_ref: Optional[str] = None
    video_ref: Optional[str] = None


class CreateCommentForPostResponse(BaseModel):
    comment_id: int
    post_id: int
    team_member_creator_id: int
    parent_comment_id: Optional[int] = None
    text: Optional[str] = None
    img_ref: Optional[str] = None
    file_ref: Optional[str] = None
    audio_ref: Optional[str] = None
    video_ref: Optional[str] = None


class ApplyJoinTeamRequest(BaseModel):
    user_id: int
    username: str
    email: str
    team_id: int


class ApplyJoinTeamResponse(BaseModel):
    id: int
    user_id: int
    username: str
    email: str
    team_id: int


class GetTeamByReferenceResponse(BaseModel):
    id: int
    name: str
    description: str
    img_profile_ref: str
    team_ref: str
    user_creator_id: int


class UserDTO(BaseModel):
    user_id: int
    username: str
    email: str


class GetPendingRequestsForTeamResponse(BaseModel):
    requests: List[UserDTO]


class AcceptPendingRequestForTeamRequest(BaseModel):
    user_id: int
    team_id: int
    username: str


class AcceptPendingRequestForTeamResponse(BaseModel):
    id: int
    user_id: int
    team_id: int
    username: str
    role: str


class RejectPendingRequestForTeamRequest(BaseModel):
    user_id: int
    team_id: int


class ChangeUserRoleInTeamRequest(BaseModel):
    user_id: int
    user_role: str
    team_id: int


class ChangeUserRoleInTeamResponse(BaseModel):
    user_id: int
    role: str
    team_id: int


class PostDTO(BaseModel):
    post_id: int
    team_id: int
    team_member_creator_id: int
    team_member_creator_username: str
    # created_at: datetime.datetime
    text: str
    img_ref: str
    file_ref: str
    audio_ref: str
    video_ref: str


class GetPostsForTeamResponse(BaseModel):
    posts: List[PostDTO]
