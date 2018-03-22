INSERT INTO "user" (first_name, last_name, email, password, phone, rating, active) VALUES ('Joey', 'Ferguson', 'joey@example.com', 'password', 1111111111, 5.0, TRUE);
INSERT INTO "user" (first_name, last_name, email, password, phone, rating, active) VALUES ('Jake', 'Smarrella', 'jake@example.com', 'password', 2222222222, 4.0, TRUE);
INSERT INTO "user" (first_name, last_name, email, password, phone, rating, active) VALUES ('Joe', 'Schuette', 'joe@example.com', 'password', 3333333333, 3.0, FALSE);
INSERT INTO "user" (first_name, last_name, email, password, phone, rating, active) VALUES ('Ross', 'Otto', 'ross@example.com', 'password', 4444444444, 2.0, TRUE);
INSERT INTO "user" (first_name, last_name, email, password, phone, rating, active) VALUES ('Harry', 'VanDerNoord', 'harry@example.com', 'password', 5555555555, 1.0, TRUE);

INSERT INTO post (user_id, price, quantity, product, loc, description) VALUES (1, 5.67, 10, 'Bananas', 'Upland', 'Sample Description');
INSERT INTO post (user_id, price, quantity, product, loc, description) VALUES (2, 6.00, 100, 'Strawberries', 'Indianapolis', 'Sample Description');
INSERT INTO post (user_id, price, quantity, product, loc, description) VALUES (3, 99.00, 50, 'Pears', 'Gas City', 'Sample Description');
INSERT INTO post (user_id, price, quantity, product, loc, description) VALUES (3, 99.00, 50, 'Grapes', 'Gas City', 'Sample Description');
INSERT INTO post (user_id, price, quantity, product, loc, description) VALUES (4, 1.25, 1, 'Apples', 'Marion', 'Sample Description');

INSERT INTO favorite (user_id, post_id) VALUES (1, 1);
INSERT INTO favorite (user_id, post_id) VALUES (1, 2);
INSERT INTO favorite (user_id, post_id) VALUES (1, 3);
INSERT INTO favorite (user_id, post_id) VALUES (2, 1);
INSERT INTO favorite (user_id, post_id) VALUES (3, 2);