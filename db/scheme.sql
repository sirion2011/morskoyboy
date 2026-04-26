CREATE DATABASE morskoyboy;

USE morskoyboy;

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tg_id BIGINT NOT NULL,
    name VARCHAR(100) DEFAULT '1',
    username VARCHAR(255) DEFAULT '1',
    dificulity INT DEFAULT 1,
    hod VARCHAR(100) NOT NULL,
    lives INT DEFAULT 3,
    game_at DATETIME NOT NULL,
    referral_id INT DEFAULT 0,
    extra_life INT DEFAULT 0
);

DESCRIBE users;
