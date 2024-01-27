CREATE TABLE IF NOT EXISTS volumes (
    id SERIAL PRIMARY KEY,
    volume_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS backups (
    id SERIAL PRIMARY KEY,
    backup_name VARCHAR(100) NOT NULL,
    volume INT NOT NULL,
    backup_date TIMESTAMP,
    FOREIGN KEY (volume) 
      REFERENCES volumes (id)
); 