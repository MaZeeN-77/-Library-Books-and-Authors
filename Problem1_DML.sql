
INSERT INTO DEPARTMENT (Dnumber, Dname, mgr_ssn, mgr_start_date)
VALUES (1, 'Research', NULL, NULL);

INSERT INTO DEPARTMENT (Dnumber, Dname, mgr_ssn, mgr_start_date)
VALUES (2, 'Administration', NULL, NULL);

INSERT INTO DEPARTMENT (Dnumber, Dname, mgr_ssn, mgr_start_date)
VALUES (3, 'Head', NULL, NULL);
GO



INSERT INTO EMPLOYEE (ssn, fname, lname, bdate, address, gender, salary, Dno)
VALUES ('1','Ahmed','Hassan','1985-03-12','Alexandria','M',8000.00,1);

INSERT INTO EMPLOYEE (ssn, fname, lname, bdate, address, gender, salary, Dno)
VALUES ('2','Sara','Ali','1990-07-25','Cairo','F',7000.00,2);

INSERT INTO EMPLOYEE (ssn, fname, lname, bdate, address, gender, salary, Dno)
VALUES ('3','Omar','Mostafa','1988-11-02','Giza','M',9000.00,3);

INSERT INTO EMPLOYEE (ssn, fname, lname, bdate, address, gender, salary, Dno)
VALUES ('4','Mona','Khaled','1995-01-18','Alexandria','F',6000.00,1);
GO

UPDATE DEPARTMENT SET mgr_ssn = '1', mgr_start_date = '2015-01-01' WHERE Dnumber = 1;
UPDATE DEPARTMENT SET mgr_ssn = '2', mgr_start_date = '2018-06-15' WHERE Dnumber = 2;
UPDATE DEPARTMENT SET mgr_ssn = '3', mgr_start_date = '2020-09-01' WHERE Dnumber = 3;
GO

INSERT INTO PROJECT (Pnumber, Pname, Plocation, Dno)
VALUES (10, 'ProductX', 'Alexandria', 1);

INSERT INTO PROJECT (Pnumber, Pname, Plocation, Dno)
VALUES (20, 'ProductY', 'Cairo', 2);

INSERT INTO PROJECT (Pnumber, Pname, Plocation, Dno)
VALUES (30, 'Computerization', 'Giza', 3);
GO

select * from [dbo].[DEPARTMENT]
select * from [dbo].[EMPLOYEE]
select * from [dbo].[PROJECT]