CREATE TABLE volumes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    volume_name VARCHAR(255),
);

CREATE TABLE backups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    volume INTEGER NOT NULL,
    backup_date datetime,
); 