from db import db
from sqlalchemy import text
import users

def get_posts_front_page(offset = 0):
    sql = text("""
    SELECT posts.*, COALESCE(sum(votes.vote), 0) as sum
    FROM posts
    LEFT JOIN votes ON posts.id = votes.post_id
    WHERE posts.hidden = FAlSE
    GROUP BY posts.id
    ORDER BY sum DESC
    LIMIT 10 OFFSET :offset
    """)
    result = db.session.execute(sql, {"offset":offset})
    return result.fetchall()

def get_posts_by_newest(offset = 0):
    sql = text("""
    SELECT posts.*, COALESCE(sum(votes.vote), 0) as sum
    FROM posts
    LEFT JOIN votes ON posts.id = votes.post_id
    WHERE posts.hidden = FAlSE
    GROUP BY posts.id
    ORDER BY created_at DESC
    LIMIT 10 OFFSET :offset
    """)
    result = db.session.execute(sql, {"offset":offset})
    return result.fetchall()

def get_posts_by_oldest(offset = 0):
    sql = text("""
    SELECT posts.*, COALESCE(sum(votes.vote), 0) as sum
    FROM posts
    LEFT JOIN votes ON posts.id = votes.post_id
    WHERE posts.hidden = FAlSE
    GROUP BY posts.id
    ORDER BY created_at ASC
    LIMIT 10 OFFSET :offset
    """)
    result = db.session.execute(sql, {"offset":offset})
    return result.fetchall()

def get_posts_by_most_votes(offset = 0):
    sql = text("""
    SELECT posts.*, COALESCE(sum(votes.vote), 0) as sum
    FROM posts
    LEFT JOIN votes ON posts.id = votes.post_id
    WHERE posts.hidden = FAlSE
    GROUP BY posts.id
    ORDER BY sum DESC
    LIMIT 10 OFFSET :offset
    """)
    result = db.session.execute(sql, {"offset":offset})
    return result.fetchall()

def get_posts_by_least_votes(offset = 0):
    sql = text("""
    SELECT posts.*, COALESCE(sum(votes.vote), 0) as sum
    FROM posts
    LEFT JOIN votes ON posts.id = votes.post_id
    WHERE posts.hidden = FAlSE
    GROUP BY posts.id
    ORDER BY sum ASC
    LIMIT 10 OFFSET :offset
    """)
    result = db.session.execute(sql, {"offset":offset})
    return result.fetchall()

def get_posts_by_most_comments(offset = 0):
    sql = text("""
    SELECT posts.*, COALESCE(sum, 0) as sum, COALESCE(count, 0) as count
    FROM posts
    LEFT JOIN (
    SELECT post_id, sum(votes.vote) as sum
    FROM votes
    GROUP BY post_id
    ) AS sums ON posts.id = sums.post_id
    LEFT JOIN (
    SELECT post_id, COUNT(comments.id) AS count
    FROM comments
    GROUP BY post_id
    ) AS counts ON posts.id = counts.post_id
    WHERE posts.hidden = FAlSE
    GROUP BY posts.id, sum, count
    ORDER BY count DESC
    LIMIT 10 OFFSET :offset
    """)
    result = db.session.execute(sql, {"offset":offset})
    return result.fetchall()

def get_posts_by_least_comments(offset = 0):
    sql = text("""
    SELECT posts.*, COALESCE(sum, 0) as sum, COALESCE(count, 0) as count
    FROM posts
    LEFT JOIN (
    SELECT post_id, sum(votes.vote) as sum
    FROM votes
    GROUP BY post_id
    ) AS sums ON posts.id = sums.post_id
    LEFT JOIN (
    SELECT post_id, COUNT(comments.id) AS count
    FROM comments
    GROUP BY post_id
    ) AS counts ON posts.id = counts.post_id
    WHERE posts.hidden = FAlSE
    GROUP BY posts.id, sum, count
    ORDER BY count ASC
    LIMIT 10 OFFSET :offset
    """)
    result = db.session.execute(sql, {"offset":offset})
    return result.fetchall()

def get_post(id):
    sql = text("SELECT * FROM posts WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def send(title, url):
    user_id = users.user_id()
    if user_id == 0:
        return False

    sql = text("INSERT INTO posts (title, url, user_id) VALUES (:title, :url, :user_id)")
    db.session.execute(sql, {"title":title, "url":url, "user_id":user_id})
    db.session.commit()
    return True

def get_posts_by_user(user_id):
    sql = text("SELECT * FROM posts WHERE user_id=:user_id")
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def edit_post(title, url, id):
    if users.user_id() == 0:
        return False

    sql = text("UPDATE posts SET (title, url) = (:title, :url) WHERE posts.id=:id")
    db.session.execute(sql, {"title":title, "url":url, "id":id})
    db.session.commit()
    return True

def hide_post(post_id):
    if users.user_id() == 0:
        return False

    sql = text("""
    UPDATE posts
    SET hidden=TRUE
    WHERE posts.id=:post_id
    """)
    db.session.execute(sql, {"post_id":post_id})
    db.session.commit()
    return True

def search(query):
    sql = text("""
    SELECT *
    FROM posts
    WHERE posts.hidden = FAlSE
    AND ((title LIKE :query)
    OR (url LIKE :query))
    """)
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    return result.fetchall()
