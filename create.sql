START TRANSACTION;
DROP TABLE IF EXISTS Users, Keywords, QuizletDecks, UsersDecks, KeywordsQuizletDecks, KeywordsUsersDecks;

CREATE TABLE `Users` (
`user_id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
`name` varchar(1024) NOT NULL,
`prefrences` varchar(1024) NOT NULL
) ENGINE = Innodb;

CREATE TABLE `Keywords` (
`keyword_id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
`keyword` varchar(1024) NOT NULL,
`created` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE = Innodb;

CREATE TABLE `QuizletDecks` (
`quizlet_id` int UNSIGNED NULL,
`json` TEXT NULL
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
`quizlet_id` int NOT NULL REFERENCES `QuizletDecks` (`quizlet_id`)
) ENGINE = Innodb;

CREATE TABLE `KeywordsUsersDecks` (
`keyword_id` int NOT NULL REFERENCES `Keywords` (`keyword_id`),
`deck_id` int NOT NULL REFERENCES `UserDecks` (`deck_id`)
) ENGINE = Innodb;
COMMIT;

-- Users(user_id, name, prefrences)
-- Keywords(keyword_id, keyword, created)
-- QuizletDecks(quizlet_id, json)
-- UserDecks(deck_id, user_id, created_on, json, longitude, latitude)
-- KeywordsQuizletDecks(keyword_id, quizlet_id)
-- KeywordsUsersDecks(keyword_id, deck_id)