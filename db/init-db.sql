INSERT INTO "user" (name, email, password, rating, active) VALUES ('Joey Ferguson', 'joey@example.com', 'password1!', 5.0, TRUE);
INSERT INTO "user" (name, email, password, rating, active) VALUES ('Jake Smarrella', 'jake@example.com', 'password1!', 4.0, TRUE);
INSERT INTO "user" (name, email, password, rating, active) VALUES ('Joe Schuette', 'joe@example.com', 'password1!', 3.0, TRUE);
INSERT INTO "user" (name, email, password, rating, active) VALUES ('Ross Otto', 'ross@example.com', 'password1!', 2.0, TRUE);
INSERT INTO "user" (name, email, password, rating, active) VALUES ('Harry VanDerNoord', 'harry@example.com', 'password1!', 1.0, TRUE);

INSERT INTO post (user_id, price, quantity, product, category, zip, description) VALUES (1, 5.67, 10, 'Carrots', 'Vegetables', 46989, 'Sample Description');
INSERT INTO post (user_id, price, quantity, product, category, zip, description) VALUES (2, 6.00, 100, 'Strawberries', 'Fruits', 56718, 'Sample Description');
INSERT INTO post (user_id, price, quantity, product, category, zip, description) VALUES (3, 99.00, 50, 'Beef', 'Meat', 89345, 'Sample Description');
INSERT INTO post (user_id, price, quantity, product, category, zip, description) VALUES (3, 99.00, 50, 'Milk', 'Dairy', 71834, 'Sample Description');
INSERT INTO post (user_id, price, quantity, product, category, zip, description) VALUES (4, 1.25, 1, 'Bread', 'Grains', 55317, 'Sample Description');

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