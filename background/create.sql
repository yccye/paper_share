# group
CREATE TABLE `group` (
  `group_id` int NOT NULL AUTO_INCREMENT,
  `group_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `num` int DEFAULT NULL,
  `time` timestamp(6) NULL DEFAULT NULL,
  `private` char(10) DEFAULT NULL,
  `description` text,
  `email` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`group_id`)
);


# group_list
CREATE TABLE `group_list` (
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  KEY `group_id` (`group_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `group_id` FOREIGN KEY (`group_id`) REFERENCES `group` (`group_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TRIGGER `delete_user` AFTER DELETE ON `group_list` FOR EACH ROW insert into logs(action,user_id,id,time) values ('退出了小组',old.user_id,old.group_id,NOW());
CREATE TRIGGER `add_user` AFTER INSERT ON `group_list` FOR EACH ROW insert into logs(action,user_id,id,time) values ('加入了小组',new.user_id,new.group_id,NOW());
CREATE TRIGGER `add_num` AFTER INSERT ON `group_list` FOR EACH ROW update `group` set num = num + 1 where group_id = new.group_id;

# paper
CREATE TABLE `paper` (
  `paper_id` int NOT NULL AUTO_INCREMENT,
  `author` varchar(255) DEFAULT NULL,
  `source` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `link` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`paper_id`)
);

# paper_list
CREATE TABLE `record_list` (
  `paper_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `group_id` int DEFAULT NULL,
  KEY `paper_id` (`paper_id`),
  KEY `user_id2` (`user_id`),
  CONSTRAINT `paper_id` FOREIGN KEY (`paper_id`) REFERENCES `paper` (`paper_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `user_id2` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TRIGGER `add_paper` AFTER INSERT ON `record_list` FOR EACH ROW insert into logs(action,user_id,id,time) values ('添加了论文',new.user_id,new.paper_id,NOW());
CREATE TRIGGER `delete_paper` AFTER DELETE ON `record_list` FOR EACH ROW insert into logs(action,user_id,id,time) values ('删除了论文',old.user_id,old.paper_id,NOW());

# note_list
CREATE TABLE `note_list` (
  `note_id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `paper_id` int DEFAULT NULL,
  `group_id` int DEFAULT NULL,
  `content` text,
  PRIMARY KEY (`note_id`),
  KEY `paper_id1` (`paper_id`),
  KEY `user_id1` (`user_id`),
  KEY `group_id1` (`group_id`),
  CONSTRAINT `group_id1` FOREIGN KEY (`group_id`) REFERENCES `group` (`group_id`) ON DELETE CASCADE,
  CONSTRAINT `paper_id1` FOREIGN KEY (`paper_id`) REFERENCES `paper` (`paper_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `user_id1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TRIGGER `add_note` AFTER INSERT ON `note_list` FOR EACH ROW insert into logs(action,user_id,id,time) values ('插入了笔记',new.user_id,new.note_id,NOW());
CREATE TRIGGER `delete_note` AFTER DELETE ON `note_list` FOR EACH ROW insert into logs(action,user_id,id,time) values ('删除了笔记',old.user_id,old.note_id,NOW());

# task
CREATE TABLE `task` (
  `content` varchar(255) DEFAULT NULL,
  `time` timestamp NULL DEFAULT NULL,
  `status` int DEFAULT NULL,
  `task_id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`task_id`) USING BTREE
);

# logs
CREATE TABLE `logs` (
  `action` varchar(255) DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `id` int DEFAULT NULL,
  `time` timestamp NULL DEFAULT NULL,
  KEY `action_user` (`user_id`),
  CONSTRAINT `action_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
);

# user
CREATE TABLE `user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `pic` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
);
