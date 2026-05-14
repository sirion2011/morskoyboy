-- ===========================================
-- База данных для бота "Мистер Свин-бот" (Морской бой)
-- ===========================================

CREATE DATABASE IF NOT EXISTS morskoyboy

USE morskoyboy;

-- Таблица пользователей
CREATE TABLE IF NOT EXISTS users (
    id            INT             NOT NULL AUTO_INCREMENT,
    tg_id         BIGINT          NOT NULL UNIQUE,
    name          VARCHAR(100)    NOT NULL DEFAULT '',
    username      VARCHAR(255)    NOT NULL DEFAULT '',
    dificulity    INT             NOT NULL DEFAULT 1,
    hod           VARCHAR(100)    NOT NULL DEFAULT 'j',
    lives         INT             NOT NULL DEFAULT 3,
    game_at       DATETIME        NOT NULL DEFAULT '2023-10-31 23:19:11',
    referral_id   BIGINT          NOT NULL DEFAULT 0,
    extra_life    INT             NOT NULL DEFAULT 0,
    PRIMARY KEY (id),
    UNIQUE KEY uq_tg_id (tg_id),
    KEY idx_username (username),
    KEY idx_referral_id (referral_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Проверка структуры
DESCRIBE users;