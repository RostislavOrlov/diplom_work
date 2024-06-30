create table chats (
  chat_id serial primary key,
  name varchar
);

create table users_chats (
  record_id serial primary key, 
  chat_id int references chats(chat_id),
  user_id int,
  chat_pinned_status boolean,
  chat_unread_status boolean,
  participant_status varchar,
  username varchar
)