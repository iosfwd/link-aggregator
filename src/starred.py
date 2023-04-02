from db import db
from sqlalchemy import text
import users

def get_starred_for_user(user_id):
    sql = text("SELECT * FROM posts, starred WHERE starred.post_id=posts.id AND starred.user_id=:user_id")
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def add_starred(post_id):
    user_id = users.user_id()
    if user_id == 0:
        return False

    sql = text("""
    INSERT INTO starred (user_id, post_id)
    VALUES (:user_id, :post_id)
    ON CONFLICT (user_id, post_id)
    DO NOTHING
    """)
    db.session.execute(sql, {"user_id":user_id, "post_id":post_id})
    db.session.commit()
    return True

def remove_starred(post_id):
    user_id = users.user_id()
    if user_id == 0:
        return False

    sql = text("DELETE FROM starred WHERE starred.user_id=:user_id AND starred.post_id=:post_id")
    db.session.execute(sql, {"user_id":user_id, "post_id":post_id})
    db.session.commit()
    return True
