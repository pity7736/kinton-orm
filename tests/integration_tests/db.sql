
CREATE TABLE category (
  id SERIAL PRIMARY KEY,
  name VARCHAR(40) NOT NULL,
  description TEXT NOT NULL
);
CREATE INDEX categories_name_index ON category(name);
