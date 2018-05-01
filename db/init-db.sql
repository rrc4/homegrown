INSERT INTO "user" (name, email, password, bio, rating, active, role) VALUES ('Admin', 'admin@example.com', 'password1!', 'Administrator sample bio', 5.0, TRUE, 'admin');
INSERT INTO "user" (name, email, password, bio, rating, active) VALUES ('Joey Ferguson', 'joey@example.com', 'password1!', 'Joey Ferguson sample bio', 5.0, TRUE);
INSERT INTO "user" (name, email, password, bio, rating, active) VALUES ('Jake Smarrella', 'jake@example.com', 'password1!', 'Jake Smarrella sample bio', 4.0, TRUE);
INSERT INTO "user" (name, email, password, bio, rating, active) VALUES ('Joe Schuette', 'joe@example.com', 'password1!', 'Joe Schuette sample bio', 3.0, TRUE);
INSERT INTO "user" (name, email, password, bio, rating, active) VALUES ('Ross Otto', 'ross@example.com', 'password1!', 'Ross Otto sample bio', 2.0, TRUE);
INSERT INTO "user" (name, email, password, bio, rating, active) VALUES ('Harry VanDerNoord', 'harry@example.com', 'password1!', 'Harry VanDerNoord sample bio', 1.0, TRUE);

INSERT INTO post (user_id, price, quantity, unit, product, category, zip, description, date) VALUES (1, 5.67, 10, 'lb', 'Carrots', 'Vegetables', 46989, 'Sample Description', '2018-04-18');
INSERT INTO post (user_id, price, quantity, unit, product, category, zip, description, date) VALUES (2, 6.00, 100, 'oz', 'Strawberries', 'Fruits', 56718, 'Sample Description', '2018-04-16');
INSERT INTO post (user_id, price, quantity, unit, product, category, zip, description, date) VALUES (3, 5.00, 75, 'item', 'Beef', 'Meat', 89345, 'Sample Description', '2018-04-15');
INSERT INTO post (user_id, price, quantity, unit, product, category, zip, description, date) VALUES (3, 3.00, 50, 'gal', 'Milk', 'Dairy', 71834, 'Sample Description', '2018-04-14');
INSERT INTO post (user_id, price, quantity, unit, product, category, zip, description, date) VALUES (4, 1.25, 1, 'kg', 'Bread', 'Grains', 55317, 'Sample Description', '2018-04-13');

INSERT INTO PHOTO (id, file_path) VALUES (1, 'static/photos/file0001.jpg');
INSERT INTO PHOTO (id, file_path) VALUES (2, 'static/photos/file0002.jpg');
INSERT INTO PHOTO (id, file_path) VALUES (3, 'static/photos/file0003.jpg');
INSERT INTO PHOTO (id, file_path) VALUES (4, 'static/photos/file0004.jpg');
INSERT INTO PHOTO (id, file_path) VALUES (5, 'static/photos/file0005.jpg');

INSERT INTO favorite (user_id, post_id) VALUES (1, 1);
INSERT INTO favorite (user_id, post_id) VALUES (1, 2);
INSERT INTO favorite (user_id, post_id) VALUES (1, 3);
INSERT INTO favorite (user_id, post_id) VALUES (2, 1);
INSERT INTO favorite (user_id, post_id) VALUES (3, 2);