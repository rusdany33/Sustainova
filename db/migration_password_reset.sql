CREATE TABLE IF NOT EXISTS password_reset_tokens (
  user_id INT NOT NULL PRIMARY KEY,
  token_hash CHAR(64) NULL UNIQUE,
  expires_at DATETIME NOT NULL,
  requested_at DATETIME NOT NULL,
  used_at DATETIME NULL,
  FOREIGN KEY (user_id) REFERENCES users(ID_user) ON DELETE CASCADE
) ENGINE=InnoDB;
