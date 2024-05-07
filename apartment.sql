create database apartment;
use apartment;

CREATE TABLE Apartments (
    apartment_id INT AUTO_INCREMENT PRIMARY KEY,
    apartment_number INT,
    area DECIMAL(10,2),
    rent DECIMAL(10,2)
);

CREATE TABLE Tenants (
    tenant_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    mobile_number VARCHAR(15),
    apartment_id INT,
    FOREIGN KEY (apartment_id) REFERENCES Apartments(apartment_id) ON DELETE CASCADE
);
