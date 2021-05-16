DROP DATABASE IF EXISTS GERAS;
CREATE DATABASE GERAS;
USE GERAS;

DROP TABLE IF EXISTS Medicine_Update;
DROP TABLE IF EXISTS Elderly;
DROP TABLE IF EXISTS Family;
DROP TABLE IF EXISTS Appoints_HW;
DROP TABLE IF EXISTS Healthcare_Worker;
DROP TABLE IF EXISTS Appoints_NGO;
DROP TABLE IF EXISTS Service;
DROP TABLE IF EXISTS Government_Officer;
DROP TABLE IF EXISTS Volunteer_NGO;
DROP TABLE IF EXISTS Volunteer;
DROP TABLE IF EXISTS NGO;



CREATE TABLE Family (
    F_ID varchar(12) NOT NULL UNIQUE,
    First_Name varchar(40) NOT NULL,
    Last_Name varchar(40) NOT NULL,
    Mobile_No varchar(10) NOT NULL UNIQUE,
    Email_ID varchar(80) NOT NULL UNIQUE,
    House_No varchar(10) NOT NULL,
    Street_Name varchar(50) NOT NULL,
    City varchar(50) NOT NULL,
    State varchar(50) NOT NULL,
    Zip varchar(6) NOT NULL,
       PRIMARY KEY(F_ID)
);

CREATE TABLE Elderly (
    Aadhar_No varchar(12) NOT NULL UNIQUE,
    First_Name varchar(50) NOT NULL,
    Last_Name varchar(50) NOT NULL,
    DOB date NOT NULL,
    Mobile_No varchar(10) NOT NULL UNIQUE,
    House_No varchar(10) NOT NULL,
    Street_Name varchar(50) NOT NULL,
    City varchar(50) NOT NULL,
    State varchar(50) NOT NULL,
    Zip varchar(6) NOT NULL,
    F_ID varchar(12),
       PRIMARY KEY(Aadhar_No)
);

CREATE TABLE Medicine_Update (
    Aadhar_No varchar(12) NOT NULL,
    Date date NOT NULL,
    Prescription varchar(400) NOT NULL,
    Doctor_Name varchar(50) NOT NULL,
    PRIMARY KEY(Aadhar_No,Date)
);





CREATE TABLE Healthcare_Worker (
    HW_ID varchar(12) NOT NULL,
    First_Name varchar(40) NOT NULL,
    Last_Name varchar(40) NOT NULL,
    Designation varchar(30) NOT NULL,
    Mobile_No varchar(10) NOT NULL UNIQUE,
    House_No varchar(10) NOT NULL,
    Street_Name varchar(50) NOT NULL,
    City varchar(50) NOT NULL,
    State varchar(50) NOT NULL,
    Zip varchar(6) NOT NULL,
    Service_Cost varchar(10) NOT NULL,
        PRIMARY KEY(HW_ID)
);

CREATE TABLE Government_Officer (
    Officer_ID varchar(12) NOT NULL,
    First_Name varchar(40) NOT NULL,
    Last_Name varchar(34) NOT NULL,
    Designation varchar(30) NOT NULL,
    Mobile_No varchar(10) NOT NULL UNIQUE,
    House_No varchar(10) NOT NULL,
    Street_Name varchar(50) NOT NULL,
    City varchar(50) NOT NULL,
    State varchar(50) NOT NULL,
    Zip varchar(6) NOT NULL,
    Email varchar(80) NOT NULL UNIQUE,
        PRIMARY KEY(Officer_ID)
);


CREATE TABLE Service (
    Service_ID varchar(12) NOT NULL,
    Details varchar(400) NOT NULL,
    Service_Status varchar(10) NOT NULL,
    Aadhar_No VARCHAR(12) NOT NULL,
    Start_Date date NOT NULL,
    End_Date date,
    Type varchar(5),
    PRIMARY KEY(Service_ID)
);

CREATE TABLE Appoints_HW (
    Service_ID varchar(12) NOT NULL UNIQUE,
    Officer_ID varchar(12) NOT NULL,
    HW_ID varchar(12) NOT NULL,
    Is_Completed VARCHAR(10) NOT NULL,
    Transaction_ID varchar(12) UNIQUE,
    Service_Cost varchar(7) NOT NULL,
    PRIMARY KEY(Service_ID)
);

CREATE TABLE Appoints_NGO (
    Service_ID varchar(12) NOT NULL,
    Officer_ID varchar(12) NOT NULL,
    NGO_ID varchar(12) NOT NULL,
    Is_Given_Vol VARCHAR(10) NOT NULL,
    Volunteer_ID varchar(12),
    Is_Completed VARCHAR(10) NOT NULL,
    Transaction_ID varchar(12) UNIQUE,
    Service_Cost varchar(4) NOT NULL,
    PRIMARY KEY(Service_ID)
);

CREATE TABLE Volunteer_NGO (
    Volunteer_ID varchar(12) NOT NULL,
    NGO_ID varchar(12) NOT NULL,
    Available varchar(10) NOT NULL,
    PRIMARY KEY(Volunteer_ID,NGO_ID)
);


CREATE TABLE Volunteer (
    Volunteer_ID varchar(12) NOT NULL,
    First_Name varchar(40) NOT NULL,
    Last_Name varchar(40) NOT NULL,
    Mobile_No varchar(10) NOT NULL UNIQUE,
    Email_ID varchar(80) NOT NULL UNIQUE,
    House_No varchar(10) NOT NULL,
    Street_Name varchar(50) NOT NULL,
    City varchar(50) NOT NULL,
    State varchar(50) NOT NULL,
    Zip varchar(6) NOT NULL,
        PRIMARY KEY(Volunteer_ID)
);

CREATE TABLE NGO (
    NGO_ID varchar(12) NOT NULL,
    Name varchar(30) NOT NULL,
    Helpline_1 varchar(11) NOT NULL UNIQUE,
    Helpline_2 varchar(11) UNIQUE,
    House_No varchar(10) NOT NULL,
    Street_Name varchar(50) NOT NULL,
    City varchar(50) NOT NULL,
    State varchar(50) NOT NULL,
    Zip varchar(6) NOT NULL,
    Website varchar(50) UNIQUE,
    Issue_Type varchar(30) NOT NULL,
    Service_Cost varchar(5) NOT NULL,
    PRIMARY KEY(NGO_ID)
);

ALTER TABLE Elderly
ADD FOREIGN KEY (F_ID) REFERENCES Family(F_ID);

ALTER TABLE Service ADD FOREIGN KEY (Aadhar_No) REFERENCES Elderly (Aadhar_No);

ALTER TABLE Appoints_NGO
ADD FOREIGN KEY (Service_ID) REFERENCES Service (Service_ID);

ALTER TABLE Appoints_NGO
ADD FOREIGN KEY (Officer_ID) REFERENCES Government_Officer (Officer_ID);

ALTER TABLE Appoints_NGO
ADD FOREIGN KEY (NGO_ID) REFERENCES NGO (NGO_ID);

ALTER TABLE Appoints_NGO
ADD FOREIGN KEY (Volunteer_ID) REFERENCES Volunteer (Volunteer_ID);

ALTER TABLE Volunteer_NGO
ADD FOREIGN KEY (Volunteer_ID) REFERENCES Volunteer (Volunteer_ID);

ALTER TABLE Volunteer_NGO
ADD FOREIGN KEY (NGO_ID) REFERENCES NGO (NGO_ID);

ALTER TABLE Appoints_HW
ADD FOREIGN KEY (Service_ID) REFERENCES Service (Service_ID);

ALTER TABLE Appoints_HW
ADD FOREIGN KEY (Officer_ID) REFERENCES Government_Officer (Officer_ID);

ALTER TABLE Appoints_HW
ADD FOREIGN KEY (HW_ID) REFERENCES Healthcare_Worker (HW_ID);

ALTER TABLE Medicine_Update
ADD FOREIGN KEY (Aadhar_No) REFERENCES Elderly (Aadhar_No);

