CREATE TABLE `location`(
    `location_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `city_id` BIGINT UNSIGNED NOT NULL,
    `latitude` DECIMAL(10, 8) NOT NULL,
    `longitude` DECIMAL(11, 8) NOT NULL,
    CONSTRAINT `location` UNIQUE (`city_id`, `latitude`, `longitude`)
);

CREATE TABLE `climate_condition`(
    `climate_condition_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `city_id` BIGINT UNSIGNED NOT NULL,
    `date` TIMESTAMP NOT NULL,
    `weather_condition` VARCHAR(255),
    `wind_speed` DECIMAL(8, 2),
    `wind_deg` SMALLINT,
    `humidity` DECIMAL(5, 2),
    `clouds` DECIMAL(8, 2)
);

CREATE TABLE `city`(
    `city_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `country_code` SMALLINT NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `state` VARCHAR(255) NULL,
    CONSTRAINT `city` UNIQUE (`country_code`, `name`, `state`)
);

CREATE TABLE `country`(
    `country_code` SMALLINT NOT NULL PRIMARY KEY,
    `country` VARCHAR(255) NOT NULL,
    `country_alpha_2` CHAR(2) NOT NULL
);

CREATE TABLE `temperature`(
    `temperature_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `city_id` BIGINT UNSIGNED NOT NULL,
    `date` TIMESTAMP NOT NULL,
    `temperature_c` DECIMAL(5, 2),
    `feels_temp_c` DECIMAL(5, 2)
);

ALTER TABLE
    `climate_condition` ADD CONSTRAINT `climate_condition_city_id_foreign` FOREIGN KEY(`city_id`) REFERENCES `city`(`city_id`);

ALTER TABLE
    `temperature` ADD CONSTRAINT `temperature_city_id_foreign` FOREIGN KEY(`city_id`) REFERENCES `city`(`city_id`);

ALTER TABLE
    `city` ADD CONSTRAINT `city_country_id_foreign` FOREIGN KEY(`country_code`) REFERENCES `country`(`country_code`);

ALTER TABLE
    `location` ADD CONSTRAINT `location_city_id_foreign` FOREIGN KEY(`city_id`) REFERENCES `city`(`city_id`);
