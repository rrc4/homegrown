INSERT INTO "user" (name, email, password, rating, active) VALUES ('Joey Ferguson', 'joey@example.com', 'password', 5.0, TRUE);
INSERT INTO "user" (name, email, password, rating, active) VALUES ('Jake Smarrella', 'jake@example.com', 'password', 4.0, TRUE);
INSERT INTO "user" (name, email, password, rating, active) VALUES ('Joe Schuette', 'joe@example.com', 'password', 3.0, FALSE);
INSERT INTO "user" (name, email, password, rating, active) VALUES ('Ross Otto', 'ross@example.com', 'password', 2.0, TRUE);
INSERT INTO "user" (name, email, password, rating, active) VALUES ('Harry VanDerNoord', 'harry@example.com', 'password', 1.0, TRUE);

INSERT INTO post (user_id, price, quantity, product, category, loc, description) VALUES (1, 5.67, 10, 'Carrots', 'Vegetables', 'Upland', 'Sample Description');
INSERT INTO post (user_id, price, quantity, product, category, loc, description) VALUES (2, 6.00, 100, 'Strawberries', 'Fruits', 'Indianapolis', 'Sample Description');
INSERT INTO post (user_id, price, quantity, product, category, loc, description) VALUES (3, 99.00, 50, 'Beef', 'Meat', 'Gas City', 'Sample Description');
INSERT INTO post (user_id, price, quantity, product, category, loc, description) VALUES (3, 99.00, 50, 'Milk', 'Dairy', 'Gas City', 'Sample Description');
INSERT INTO post (user_id, price, quantity, product, category, loc, description) VALUES (4, 1.25, 1, 'Bread', 'Grains', 'Marion', 'Sample Description');

INSERT INTO favorite (user_id, post_id) VALUES (1, 1);
INSERT INTO favorite (user_id, post_id) VALUES (1, 2);
INSERT INTO favorite (user_id, post_id) VALUES (1, 3);
INSERT INTO favorite (user_id, post_id) VALUES (2, 1);
INSERT INTO favorite (user_id, post_id) VALUES (3, 2);