CREATE DATABASE company;
GO

USE company;
GO

CREATE TABLE EMPLOYEE (
    ssn      CHAR(9)        NOT NULL,
    fname    VARCHAR(30)    NOT NULL,
    lname    VARCHAR(30)    NOT NULL,
    bdate    DATE,
    address  VARCHAR(100),
    gender   CHAR(1),
    salary   DECIMAL(10,2),
    Dno      INT,
    PRIMARY KEY (ssn)
);
GO

CREATE TABLE DEPARTMENT (
    Dnumber        INT           NOT NULL,
    Dname          VARCHAR(50)   NOT NULL,
    mgr_ssn        CHAR(9),
    mgr_start_date DATE,
    PRIMARY KEY (Dnumber)
);
GO

CREATE TABLE PROJECT (
    Pnumber   INT           NOT NULL,
    Pname     VARCHAR(50)   NOT NULL,
    Plocation VARCHAR(50),
    Dno       INT           NOT NULL,
    PRIMARY KEY (Pnumber)
);
GO

ALTER TABLE EMPLOYEE
    ADD CONSTRAINT fk_employee_dept
    FOREIGN KEY (Dno) REFERENCES DEPARTMENT(Dnumber);
GO

ALTER TABLE DEPARTMENT
    ADD CONSTRAINT fk_department_mgr
    FOREIGN KEY (mgr_ssn) REFERENCES EMPLOYEE(ssn);
GO

ALTER TABLE PROJECT
    ADD CONSTRAINT fk_project_dept
    FOREIGN KEY (Dno) REFERENCES DEPARTMENT(Dnumber);
GO
