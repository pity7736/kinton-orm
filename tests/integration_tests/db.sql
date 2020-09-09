
CREATE TABLE category (
  id SERIAL PRIMARY KEY,
  name VARCHAR(40) NOT NULL,
  description TEXT NOT NULL
);
CREATE INDEX categories_name_index ON category(name);

CREATE TABLE tag (
    id SERIAL PRIMARY KEY,
    name VARCHAR(40) NOT NULL
);

CREATE TABLE post (
    id SERIAL PRIMARY KEY,
    title VARCHAR(40) NOT NULL,
    category_id INTEGER REFERENCES category ON DELETE CASCADE,
    tag_id INTEGER REFERENCES tag ON DELETE CASCADE
);
