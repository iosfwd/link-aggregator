DROP TABLE IF EXISTS
     users,
     posts,
     comments,
     starred,
     votes
     CASCADE;

CREATE TABLE users (
       id SERIAL PRIMARY KEY,
       username TEXT UNIQUE NOT NULL,
       password TEXT NOT NULL,
       is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE posts (
       id SERIAL PRIMARY KEY,
       title TEXT NOT NULL,
       url TEXT NOT NULL,
       user_id INTEGER NOT NULL REFERENCES users,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       hidden BOOLEAN DEFAULT FALSE
);

CREATE TABLE comments (
       id SERIAL PRIMARY KEY,
       body TEXT NOT NULL,
       user_id INTEGER NOT NULL REFERENCES users,
       post_id INTEGER NOT NULL REFERENCES posts,
       parent_comment_id INTEGER REFERENCES comments,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       hidden BOOLEAN DEFAULT FALSE
);

CREATE TABLE starred (
       id SERIAL PRIMARY KEY,
       user_id INTEGER NOT NULL REFERENCES users,
       post_id INTEGER NOT NULL REFERENCES posts,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       UNIQUE(user_id, post_id)
);

CREATE TABLE votes (
       id SERIAL PRIMARY KEY,
       user_id INTEGER NOT NULL REFERENCES users,
       post_id INTEGER NOT NULL REFERENCES posts,
       vote INTEGER NOT NULL CHECK (vote = 1 OR vote = -1),
       UNIQUE(user_id, post_id)
);

INSERT INTO users (username, password, is_admin) VALUES ('root','pbkdf2:sha256:260000$EoeIX9SsMo07DYoI$80d77f6fafe782482cc7bf556abb670390b022a76a23890a4a5f477ef37bfac5', TRUE);
INSERT INTO users (username, password) VALUES ('doot','pbkdf2:sha256:260000$EoeIX9SsMo07DYoI$80d77f6fafe782482cc7bf556abb670390b022a76a23890a4a5f477ef37bfac5');
INSERT INTO users (username, password) VALUES ('noot','pbkdf2:sha256:260000$EoeIX9SsMo07DYoI$80d77f6fafe782482cc7bf556abb670390b022a76a23890a4a5f477ef37bfac5');


INSERT INTO posts (title, url, user_id) VALUES ('Search engine', 'https://www.google.com', 1);
INSERT INTO posts (title, url, user_id) VALUES ('Another search engine', 'https://www.bing.com', 2);
INSERT INTO posts (title, url, user_id) VALUES ('Yle', 'https://yle.fi', 3);
INSERT INTO posts (title, url, user_id) VALUES ('Hesari', 'https://hs.fi', 2);
INSERT INTO posts (title, url, user_id) VALUES ('Weather', 'https://www.foreca.fi/Finland/Helsinki/details', 1);
INSERT INTO posts (title, url, user_id) VALUES ('Github', 'https://github.com', 2);
INSERT INTO posts (title, url, user_id) VALUES ('Gitlab', 'https://gitlab.com', 3);
INSERT INTO posts (title, url, user_id) VALUES ('English Wikipedia', 'https://en.wikipedia.org', 1);
INSERT INTO posts (title, url, user_id) VALUES ('Finnish Wikipedia', 'https://fi.wikipedia.org', 2);
INSERT INTO posts (title, url, user_id) VALUES ('Study material', 'https://hy-tsoha.github.io/materiaali/', 3);
INSERT INTO posts (title, url, user_id) VALUES ('Free courses', 'https://mooc.fi', 1);

INSERT INTO comments (body, user_id, post_id) VALUES ('Good search engine', 1, 1);
INSERT INTO comments (body, user_id, post_id, parent_comment_id) VALUES ('Too much ads', 2, 1, 1);
INSERT INTO comments (body, user_id, post_id, parent_comment_id) VALUES ('I agree', 3, 1, 2);

INSERT INTO starred (user_id, post_id) VALUES (1, 1);

INSERT INTO votes (user_id, post_id, vote) VALUES (1, 1, 1);
INSERT INTO votes (user_id, post_id, vote) VALUES (2, 1, 1);
INSERT INTO votes (user_id, post_id, vote) VALUES (3, 1, 1);
