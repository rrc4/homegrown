DROP TABLE IF EXISTS "user";
DROP TABLE IF EXISTS post;

CREATE TABLE "user"
(
  id SERIAL PRIMARY KEY,
  first_name VARCHAR(40) NOT NULL,
  last_name VARCHAR(40) NOT NULL,
  email VARCHAR(40) NOT NULL,
  password VARCHAR(40) NOT NULL,
  phone VARCHAR(10) NOT NULL,
  rating FLOAT NOT NULL,
  active BOOLEAN NOT NULL
);
CREATE UNIQUE INDEX user_id_index ON "user" (id);
COMMENT ON TABLE "user" IS 'User';

CREATE TABLE post
(
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES "user",
  price FLOAT NOT NULL,
  quantity INTEGER NOT NULL,
  product VARCHAR(40) NOT NULL,
  loc VARCHAR(40) NOT NULL,
  description VARCHAR(150) NOT NULL
);
CREATE UNIQUE INDEX post_id_index ON post (id);
COMMENT ON TABLE post IS 'Post';
