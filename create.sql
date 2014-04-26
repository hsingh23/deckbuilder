START TRANSACTION;
SET GLOBAL general_log='OFF';
DROP TABLE IF EXISTS Users, Keywords, QuizletDecks, UserDecks, KeywordsQuizletDecks, KeywordsUserDecks;
DROP PROCEDURE create_or_update_quizlet;

CREATE TABLE `Users` (
`user_id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
`name` varchar(1024) NOT NULL,
`prefrences` varchar(1024) NOT NULL
) ENGINE = Innodb;

CREATE TABLE `Keywords` (
`keyword_id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
`keyword` varchar(1024) NOT NULL,
`last_updated` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE = Innodb;

CREATE TABLE `QuizletDecks` (
`quizlet_id` int UNSIGNED NULL,
`json` TEXT NULL,
) ENGINE = Innodb;

CREATE TABLE `UserDecks` (
`deck_id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
`user_id` int NOT NULL REFERENCES `Users` (`user_id`),
`created_on` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
`json` TEXT NULL,
`latitude` float(10,6) NULL,
`longitude` float(10,6) NULL
) ENGINE = Innodb;

-- Join Tables (Many to Many)
CREATE TABLE `KeywordsQuizletDecks` (
`keyword_id` int NOT NULL REFERENCES `Keywords` (`keyword_id`),
`quizlet_id` int NOT NULL REFERENCES `QuizletDecks` (`quizlet_id`),
`terms_selected` INT UNSIGNED  DEFAULT 0,
`times_deck_selected` INT UNSIGNED DEFAULT 0
) ENGINE = Innodb;

CREATE TABLE `KeywordsUserDecks` (
`keyword_id` int NOT NULL REFERENCES `Keywords` (`keyword_id`),
`deck_id` int NOT NULL REFERENCES `UserDecks` (`deck_id`)
) ENGINE = Innodb;

DELIMITER //
CREATE PROCEDURE create_or_update_quizlet
(IN new_quizlet_id INT UNSIGNED, new_keyword_id INT UNSIGNED, new_json TEXT)
MODIFIES SQL DATA
BEGIN
IF NOT EXISTS (SELECT quizlet_id FROM QuizletDecks WHERE quizlet_id = new_quizlet_id) 
THEN
  INSERT INTO QuizletDecks (quizlet_id, json) VALUES (new_quizlet_id, new_json);
  INSERT INTO KeywordsQuizletDecks (quizlet_id, keyword_id) VALUES (new_quizlet_id, new_keyword_id);
ELSE
  UPDATE QuizletDecks SET json = new_json WHERE quizlet_id = new_quizlet_id;
END IF;
END;//
DELIMITER ;
COMMIT;


-- Users(user_id, name, prefrences)
-- Keywords(keyword_id, keyword, created)
-- QuizletDecks(quizlet_id, json, terms_selected, times_deck_selected)
-- UserDecks(deck_id, user_id, created_on, json, longitude, latitude)
-- KeywordsQuizletDecks(keyword_id, quizlet_id)
-- KeywordsUsersDecks(keyword_id, deck_id)