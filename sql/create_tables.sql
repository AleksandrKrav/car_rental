CREATE TABLE rental_car.users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    role VARCHAR(50) NOT NULL
);

CREATE TABLE rental_car.cars (
    id INT AUTO_INCREMENT PRIMARY KEY,
    license_plate VARCHAR(20) NOT NULL UNIQUE,
    status VARCHAR(50) NOT NULL,
    car_type VARCHAR(50) NOT NULL
);

CREATE TABLE rental_car.orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    car_id INT NOT NULL,
    order_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    price INT NOT NULL,
    payment_status BOOL,
    rental_start_date DATETIME NOT NULL,
    rental_end_date DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES rental_car.users(id) ON DELETE CASCADE,
    FOREIGN KEY (car_id) REFERENCES rental_car.cars(id) ON DELETE CASCADE,
    CHECK (DATEDIFF(rental_start_date, rental_end_date) <= 7)
);

CREATE TABLE rental_car.payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES rental_car.orders(id) ON DELETE CASCADE
);
