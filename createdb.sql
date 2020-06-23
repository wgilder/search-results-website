CREATE TABLE `items` (
  `url` varchar(2048) NOT NULL,
  `type` varchar(40) NOT NULL,
  `title` varchar(256) NOT NULL,
  `description` text NOT NULL,
  `creationDate` datetime NOT NULL,
  `modificationDate` datetime NOT NULL,
  KEY `type` (`type`),
  KEY `creationDate` (`creationDate`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;