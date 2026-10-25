
use library

INSERT INTO AUTHOR (name, country) VALUES ('Ahmed Khaled Tawfik', 'Egypt');
INSERT INTO AUTHOR (name, country) VALUES ('J.K. Rowling', 'United Kingdom');
INSERT INTO AUTHOR (name, country) VALUES ('Dan Brown', 'United States');
GO

INSERT INTO BOOK (title, price, author_id) VALUES ('Utopia', 15.50, 1);
INSERT INTO BOOK (title, price, author_id) VALUES ('Vertigo', 12.00, 1);
INSERT INTO BOOK (title, price, author_id) VALUES ('Harry Potter and the Philosopher''s Stone', 18.75, 2);
INSERT INTO BOOK (title, price, author_id) VALUES ('Harry Potter and the Chamber of Secrets', 16.00, 2);
INSERT INTO BOOK (title, price, author_id) VALUES ('The Da Vinci Code', 14.25, 3);
INSERT INTO BOOK (title, price, author_id) VALUES ('Angels and Demons', 11.50, 3);
GO