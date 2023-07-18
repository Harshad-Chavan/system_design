---- this use is created to access the auth database
--CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'Aauth123';
--
---- create a database to be used by the auth service
--CREATE DATABASE auth;
--
---- grant permission to the user create abpve
--GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';
--
--USE auth;

CREATE TABLE user(
id INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
email VARCHAR(255) NOT NULL UNIQUE,
password VARCHAR(255) NOT NULL
)

INSERT INTO user(email,password) VALUES('harshad@emaipwsl.com','admin123');