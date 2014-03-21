START TRANSACTION;
DROP TABLE IF EXISTS Keyword, Deck, KeywordDeck, Card, CardDeck;
CREATE TABLE `Keyword` (
`kid` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
`text` varchar(4000) NOT NULL
) ENGINE = MYISAM;

CREATE TABLE `Deck` (
`did` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
`qid` int UNSIGNED NULL UNIQUE,
`url` varchar(2000) NULL,
`title` varchar(2000) NULL,
`qcreated_by` varchar(255) NULL,
`qterm_count` smallint UNSIGNED NOT NULL,
`qcreated_date` int NULL,
`qmodified_date` int NULL,
`qhas_images` enum('False','True') NULL DEFAULT NULL,
`qsubject` varchar(3000) NULL,
`qdescription` varchar(4000) NULL,
`qlang_term` varchar(255) NULL,
`qlang_definitions` varchar(255) NULL,
`qhas_discussion` enum('False','True') NULL DEFAULT NULL
) ENGINE = MYISAM;

CREATE TABLE `KeywordDeck` (
`kid` int NOT NULL REFERENCES `Keyword` (`kid`),
`did` int NOT NULL REFERENCES `Card` (`cid`)
) ENGINE = MYISAM;

CREATE TABLE `Card` (
`cid` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
`front` varchar(8000) NULL,
`back` varchar(8000) NULL,
`position` smallint NULL
) ENGINE = MYISAM;

CREATE TABLE `CardDeck` (
`cid` int NOT NULL REFERENCES `Card` (`cid`),
`did` int NOT NULL REFERENCES `Deck` (`cid`)
) ENGINE = MYISAM;

CREATE VIEW FullTable AS SELECT * FROM Keyword NATURAL JOIN KeywordDeck NATURAL JOIN Deck NATURAL JOIN CardDeck NATURAL JOIN Card;
CREATE TRIGGER fill_join_table BEFORE INSERT ON FullTable
FOR EACH ROW 
BEGIN
   
END
COMMIT;