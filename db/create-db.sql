DROP TABLE IF EXISTS favorite;
DROP TABLE IF EXISTS photo;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS "user";

CREATE TABLE "user"
(
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(40) NOT NULL,
    password VARCHAR(40) NOT NULL,
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
    category VARCHAR(10) NOT NULL,
    CHECK (category = 'Vegetables' OR
           category = 'Fruits' OR
           category = 'Meat' OR
           category = 'Dairy' OR
           category = 'Grains' OR
           category = 'Other'),
    zip VARCHAR(9) NOT NULL,
    description VARCHAR(150) NOT NULL
);
CREATE UNIQUE INDEX post_id_index ON post (id);
COMMENT ON TABLE post IS 'Post';

CREATE TABLE photo
(
  id SERIAL NOT NULL CONSTRAINT photo_pkey PRIMARY KEY REFERENCES post,
  file_path VARCHAR(255) NOT NULL DEFAULT 'bogus-path'
);
COMMENT ON TABLE photo IS 'Photo';

CREATE TABLE favorite
(
    post_id INTEGER NOT NULL REFERENCES post (id),
    user_id INTEGER NOT NULL REFERENCES "user" (id)
);
CREATE UNIQUE INDEX favorite_id_index on post (id);
COMMENT ON TABLE favorite IS 'Favorite';
