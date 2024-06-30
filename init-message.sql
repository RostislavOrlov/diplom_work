create table messages (
    message_id serial primary key,
    sender_id int,
    sender_username varchar,
    chat_id int,
    message_text varchar,
    date_of_creation date,
    edited_at date
);

create table users_messages (
    record_id serial primary key,
    user_id int,
    message_id int references messages(message_id),
    pinned_status bool,
    read_status bool,
    forward_status bool,
    reply_status bool
)
