DROP TABLE IF EXISTS member;
DROP TABLE IF EXISTS post;

CREATE TABLE member
(
  id SERIAL PRIMARY KEY,
  first_name VARCHAR(40) NOT NULL,
  last_name VARCHAR(40) NOT NULL,
  email VARCHAR(40) NOT NULL,
  password VARCHAR(40) NOT NULL,
  phone BIGINT NOT NULL,
  rating FLOAT NOT NULL,
  active BOOLEAN NOT NULL
);
CREATE UNIQUE INDEX member_id_index ON member (id);
COMMENT ON TABLE member IS 'Member';

CREATE TABLE post
(
  id SERIAL PRIMARY KEY,
  price FLOAT NOT NULL,
  quantity INTEGER NOT NULL,
  product VARCHAR(40) NOT NULL,
  loc VARCHAR(40) NOT NULL
);
CREATE UNIQUE INDEX post_id_index ON post (id);
COMMENT ON TABLE post IS 'Post';
