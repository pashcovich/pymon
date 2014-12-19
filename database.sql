
CREATE TABLE IF NOT EXISTS users (
  id integer primary key autoincrement,
  login text not null,
  password text not null,
  role integer default 0,
  active integer default 1
);


create table if not exists roles (
  id integer primary key autoincrement,
  role VARCHAR(255) not null,
  comment VARCHAR(255)
);


create table  if not exists servers (
  id integer primary key autoincrement,
  srv_id integer not null unique,
  name VARCHAR(255) not null,
  uptime VARCHAR(255) not null,
  memory VARCHAR(255) not null,
  disk VARCHAR(255) not null,
  cpu VARCHAR(255) not null,
  processes INTEGER not null

);

