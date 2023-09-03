CREATE TABLE IF NOT EXISTS volumes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    volume_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS backups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    backup_name TEXT NOT NULL UNIQUE,
    volume INTEGER NOT NULL,
    backup_date datetime,
    FOREIGN KEY (volume) 
      REFERENCES volumes (id)
); 