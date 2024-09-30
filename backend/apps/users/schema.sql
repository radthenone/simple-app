CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    is_active INTEGER NOT NULL,
    is_admin INTEGER NOT NULL,
    created_at DATETIME,
    updated_at DATETIME
);
