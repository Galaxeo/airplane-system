INSERT INTO `Airline` VALUES ("Jet Blue");
INSERT INTO `Airline` VALUES ("Delta");
INSERT INTO `Airport` VALUES ("JFK", "John F. Kennedy", "New York City", "United States of America", 5, "International");
INSERT INTO `Airport` VALUES ("PVG", "Shanghai Pudong", "Shanghai", "China", 2, "International");
INSERT INTO `Airport` VALUES ("SFO", "San Francisco Intenational", "San Francisco", "United States of America", 4, "International");
INSERT INTO `Customer` VALUES ("jhc737@nyu.edu", "abc123", "Justin", "Cheok", '2', 'Metrotech Center', NULL, 'Brooklyn', 'New York', '11201', 11123, '2025-12-05', 'United States of America', '2001-10-09');
INSERT INTO `CustomerPhone` VALUES ('jhc737@nyu.edu', '123-456-7890');
INSERT INTO `Customer` VALUES ('bobby@gmail.com', md5('abc123'), 'Bobby', 'Glassway', '55', 'Clark Street', '2023', 'Brooklyn', 'New York', '11203', 33321, '2023-12-03', 'United States of America', '1999-01-01');
INSERT INTO `CustomerPhone` VALUES ('bobby@gmail.com', '223-223-2223');
INSERT INTO `Customer` VALUES ('lucile@gmail.com', md5('abc123'), 'Lucile', 'Glassway', '55', 'Clark Street', '2023', 'Brooklyn', 'New York', '11203', 55231, '2025-02-23', 'United States of America', '1968-06-12');
INSERT INTO `CustomerPhone` VALUES ('lucile@gmail.com', '444-444-4444');
INSERT INTO `Airplane` VALUES (22321, 'Jet Blue', '4', 'Boeing', 'KD35', '2005-10-23', 18);
INSERT INTO `Airplane` VALUES (11231, 'Jet Blue', '189', 'Boeing', '737', '2022-11-08', 1);
INSERT INTO `Airplane` VALUES (94301, 'Jet Blue', '70', 'NYU', 'SC30', '2021-01-03', 2);
INSERT INTO `Airplane` VALUES (22326, 'Jet Blue', '50', 'Warriors', 'KT11', '2020-06-30', 3);
INSERT INTO `Airplane` VALUES (94303, 'Delta', '113', 'Cheok', 'Yokai', '2021-01-13', 3);
INSERT INTO `AirlineStaff` VALUES ('austinhao88', 'pass221', 'Jet Blue', 'Austin', 'Hao', '1999-07-29');
INSERT INTO `Flight` VALUES ('Jet Blue', 223, '2023-11-08 12:00:00', 'JFK', '2023-11-08 21:00:00', 'PVG', 0999.23, 'On-time', 22321);
INSERT INTO `Flight` VALUES ('Jet Blue', 224, '2023-11-08 18:00:00', 'JFK', '2023-11-09 05:00:00', 'PVG', 1299.23, 'On-time', 11231);
INSERT INTO `Flight` VALUES ('Jet Blue', 225, '2023-11-08 08:00:00', 'JFK', '2023-11-08 11:30:00', 'PVG', 0899.23, 'Delayed', 94301);
INSERT INTO `Flight` VALUES ('Jet Blue', 226, '2023-11-09 00:00:00', 'JFK', '2023-11-09 08:00:00', 'PVG', 0699.23, 'On-time', 22326);
INSERT INTO `Flight` VALUES ('Jet Blue', 327, DATE_ADD(CURDATE(), INTERVAL FLOOR(RAND() * 30) DAY), 'JFK', DATE_ADD(CURDATE(), INTERVAL FLOOR(RAND() * 30) DAY), 'PVG', 0999.23, 'On-time', 22321);
INSERT INTO `Flight` VALUES ('Jet Blue', 328, DATE_ADD(CURDATE(), INTERVAL FLOOR(RAND() * 30) DAY), 'JFK', DATE_ADD(CURDATE(), INTERVAL FLOOR(RAND() * 30) DAY), 'PVG', 1299.23, 'On-time', 11231);
INSERT INTO `Flight` VALUES ('Jet Blue', 329, DATE_ADD(CURDATE(), INTERVAL FLOOR(RAND() * 30) DAY), 'JFK', DATE_ADD(CURDATE(), INTERVAL FLOOR(RAND() * 30) DAY), 'PVG', 0899.23, 'Delayed', 94301);
INSERT INTO `Flight` VALUES ('Jet Blue', 330, DATE_ADD(CURDATE(), INTERVAL FLOOR(RAND() * 30) DAY), 'JFK', DATE_ADD(CURDATE(), INTERVAL FLOOR(RAND() * 30) DAY), 'PVG', 0699.23, 'On-time', 22326);
INSERT INTO `Flight` VALUES ('Delta', 430, DATE_ADD(CURDATE(), INTERVAL FLOOR(RAND() * 30) DAY), 'SFO', DATE_ADD(CURDATE(), INTERVAL FLOOR(RAND() * 30) DAY), 'JFK', 3000.11, 'On-time', 22326);
INSERT INTO `Ticket` VALUES ('0001', 223);
INSERT INTO `Ticket` VALUES ('0011', 223);
INSERT INTO `Ticket` VALUES ('0002', 224);
INSERT INTO `Ticket` VALUES ('0003', 225);
INSERT INTO `Ticket` VALUES ('0004', 226);
INSERT INTO `Ticket` VALUES ('0005', 225);
INSERT INTO `Ticket` VALUES ('0006', 225);
INSERT INTO `Ticket` VALUES ('0007', 225);
INSERT INTO `Ticket` VALUES ('0008', 225);
INSERT INTO `Ticket` VALUES ('0009', 225);
INSERT INTO `Ticket` VALUES ('0010', 225);
INSERT INTO `Ticket` VALUES ('1010', 430);
INSERT INTO `Ticket` VALUES ('1011', 430);
INSERT INTO `Ticket` VALUES ('1012', 430);
INSERT INTO `Purchase` VALUES ('0001', 'lucile@gmail.com', 'Debit', '2234 2314 2314 2314', '2023-12-26', 'Lucile Glassway', '2023-11-06 04:23:26', 1233.99, 'Lucile', 'Glassway', '1968-06-12');
INSERT INTO `Purchase` VALUES ('0011', 'lucile@gmail.com', 'Debit', '2234 2314 2314 2314', '2023-12-26', 'Lucile Glassway', '2023-11-06 04:24:12', 999.99, 'Bobby', 'Glassway', '1999-01-01');
INSERT INTO `Purchase` VALUES ('0002', 'jhc737@nyu.edu', 'Credit', '1111 1111 1111 1111', '2025-02-16', 'Justin Cheok', '2023-10-09 01:25:48', 1000.00, 'Justin', 'Cheok', '2001-10-09');
INSERT INTO `Purchase` VALUES ('1010', 'bobby@gmail.com', 'Credit', '1111 1111 1111 1111', '2025-02-16', 'df', '2023-10-09 01:25:48', 1000.00, 'Bobathan', 'Saggerton', '2001-10-09');