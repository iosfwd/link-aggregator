from db import db
from sqlalchemy import text
import users, posts

def get_votes_by_post(post_id):
    sql = text("SELECT sum(vote) FROM votes WHERE post_id=:post_id")
    result = db.session.execute(sql, {"post_id":post_id})
    return result.fetchone()

def get_votes_by_user(user_id):
    sql = text("SELECT * FROM posts WHERE user_id=:user_id")
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def get_vote_count_by_post(post_id):
    sql = text("SELECT count(*) FROM posts WHERE post_id=:post_id")
    result = db.session.execute(sql, {"post_id":post_id})
    return result.fetchone()

def add_upvote(post_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    try:
        sql = text("""
        INSERT INTO votes (user_id, post_id, vote)
        VALUES (:user_id, :post_id, 1)
        ON CONFLICT (user_id, post_id)
        DO UPDATE SET vote=1
        """)
        db.session.execute(sql, {"user_id":user_id, "post_id":post_id})
        db.session.commit()
    except:
        return False

    return True

def add_downvote(post_id):
    user_id = users.user_id()
    if user_id == 0:
        return False

    try:
        sql = text("""
        INSERT INTO votes (user_id, post_id, vote)
        VALUES (:user_id, :post_id, -1)
        ON CONFLICT (user_id, post_id)
        DO UPDATE SET vote=-1
        """)
        db.session.execute(sql, {"user_id":user_id, "post_id":post_id})
        db.session.commit()
    except:
        return False

    return True

def remove_vote(post_id):
    user_id = users.user_id()
    if user_id == 0:
        return False

    sql = text("DELETE FROM votes WHERE votes.user_id=:user_id AND votes.post_id=:post_id")
    db.session.execute(sql, {"user_id":user_id, "post_id":post_id})
    db.session.commit()
    return True
