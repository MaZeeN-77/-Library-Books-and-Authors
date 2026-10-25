CREATE DATABASE library;
GO

USE library;
GO

CREATE TABLE AUTHOR (
    author_id INT IDENTITY(1,1) NOT NULL,
    name      VARCHAR(100)  NOT NULL,
    country   VARCHAR(50),
    PRIMARY KEY (author_id)
);
GO

CREATE TABLE BOOK (
    book_id   INT IDENTITY(1,1) NOT NULL,
    title     VARCHAR(150)   NOT NULL,
    price     DECIMAL(10,2),
    author_id INT            NOT NULL,
    PRIMARY KEY (book_id),
    FOREIGN KEY (author_id) REFERENCES AUTHOR(author_id) ON DELETE CASCADE
);
GO