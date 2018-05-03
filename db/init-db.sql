INSERT INTO "user" (name, email, zip, password, bio, rating, active) VALUES ('Joey Ferguson', 'joey@example.com', 55317, 'password1!', 'Joey Ferguson sample bio', 5.0, TRUE);
INSERT INTO "user" (name, email, zip, password, bio, rating, active) VALUES ('Jake Smarrella', 'jake@example.com', 46989, 'password1!', 'Jake Smarrella sample bio', 4.0, TRUE);
INSERT INTO "user" (name, email, zip, password, bio, rating, active) VALUES ('Joe Schuette', 'joe@example.com', 21498, 'password1!', 'Joe Schuette sample bio', 3.0, TRUE);
INSERT INTO "user" (name, email, zip, password, bio, rating, active) VALUES ('Ross Otto', 'ross@example.com', 93486, 'password1!', 'Ross Otto sample bio', 2.0, TRUE);
INSERT INTO "user" (name, email, zip, password, bio, rating, active) VALUES ('Harry VanDerNoord', 'harry@example.com', 78935, 'password1!', 'Harry VanDerNoord sample bio', 1.0, TRUE);
INSERT INTO "user" (name, email, zip, password, bio, rating, active, role) VALUES ('Admin', 'admin@example.com', 10285, 'password1!', 'Administrator sample bio', 5.0, TRUE, 'admin');

INSERT INTO post (user_id, price, quantity, unit, product, category, description, date) VALUES (1, 1.00, 10, 'lb', 'Carrots', 'Vegetables', 'Sample Description', '2018-04-18');
INSERT INTO post (user_id, price, quantity, unit, product, category, description, date) VALUES (1, 6.00, 100, 'lb', 'Strawberries', 'Fruits', 'Sample Description', '2018-04-16');
INSERT INTO post (user_id, price, quantity, unit, product, category, description, date) VALUES (2, 5.00, 75, 'item', 'Beef', 'Meat', 'Sample Description', '2018-04-15');
INSERT INTO post (user_id, price, quantity, unit, product, category, description, date) VALUES (2, 3.00, 50, 'gal', 'Milk', 'Dairy', 'Sample Description', '2018-04-14');
INSERT INTO post (user_id, price, quantity, unit, product, category, description, date) VALUES (3, 1.50, 4, 'kg', 'Bread', 'Grains', 'Sample Description', '2018-04-13');
INSERT INTO post (user_id, price, quantity, unit, product, category, description, date) VALUES (3, 5.00, 75, 'item', 'Chicken Breast', 'Meat', 'Sample Description', '2018-04-15');
INSERT INTO post (user_id, price, quantity, unit, product, category, description, date) VALUES (4, 2.00, 8, 'dozen', 'Eggs', 'Dairy', 'Sample Description', '2018-04-14');
INSERT INTO post (user_id, price, quantity, unit, product, category, description, date) VALUES (4, 4.00, 6, 'lb', 'Grapes', 'Fruits', 'Sample Description', '2018-04-13');
INSERT INTO post (user_id, price, quantity, unit, product, category, description, date) VALUES (5, 1.00, 10, 'oz', 'Broccoli', 'Vegetables', 'Sample Description', '2018-04-18');
INSERT INTO post (user_id, price, quantity, unit, product, category, description, date) VALUES (5, 2.50, 100, 'item', 'Cinnamon Rolls', 'Grains', 'Sample Description', '2018-04-18');

INSERT INTO post_photo (id, file_path) VALUES (1, 'static/photos/file0001.jpg');
INSERT INTO post_photo (id, file_path) VALUES (2, 'static/photos/file0002.jpg');
INSERT INTO post_photo (id, file_path) VALUES (3, 'static/photos/file0003.jpg');
INSERT INTO post_photo (id, file_path) VALUES (4, 'static/photos/file0004.jpg');
INSERT INTO post_photo (id, file_path) VALUES (5, 'static/photos/file0005.jpg');
INSERT INTO post_photo (id, file_path) VALUES (6, 'static/photos/file0006.jpg');
INSERT INTO post_photo (id, file_path) VALUES (7, 'static/photos/file0007.jpg');
INSERT INTO post_photo (id, file_path) VALUES (8, 'static/photos/file0008.jpg');
INSERT INTO post_photo (id, file_path) VALUES (9, 'static/photos/file0009.jpg');
INSERT INTO post_photo (id, file_path) VALUES (10, 'static/photos/file0010.jpg');

INSERT INTO user_photo (id, file_path) VALUES (1, 'static/user-photos/file0001.jpg');
INSERT INTO user_photo (id, file_path) VALUES (2, 'static/user-photos/file0002.jpg');
INSERT INTO user_photo (id, file_path) VALUES (3, 'static/user-photos/file0003.jpg');
INSERT INTO user_photo (id, file_path) VALUES (4, 'static/user-photos/file0004.jpg');
INSERT INTO user_photo (id, file_path) VALUES (5, 'static/user-photos/file0005.jpg');

INSERT INTO favorite (user_id, post_id) VALUES (1, 6);
INSERT INTO favorite (user_id, post_id) VALUES (2, 7);
INSERT INTO favorite (user_id, post_id) VALUES (3, 8);
INSERT INTO favorite (user_id, post_id) VALUES (4, 9);
INSERT INTO favorite (user_id, post_id) VALUES (5, 10);
INSERT INTO favorite (user_id, post_id) VALUES (1, 2);
INSERT INTO favorite (user_id, post_id) VALUES (2, 3);
INSERT INTO favorite (user_id, post_id) VALUES (3, 4);
INSERT INTO favorite (user_id, post_id) VALUES (4, 5);
INSERT INTO favorite (user_id, post_id) VALUES (5, 1);