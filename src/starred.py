from db import db
from sqlalchemy import text
import users

def get_starred_for_user(user_id):
    sql = text("""
    SELECT * FROM stories, starred
    WHERE starred.story_id=stories.id
    AND starred.user_id=:user_id
    AND stories.hidden = FALSE
    """)
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def add_starred(story_id):
    user_id = users.user_id()
    if user_id == 0:
        return False

    sql = text("""
    INSERT INTO starred (user_id, story_id)
    VALUES (:user_id, :story_id)
    ON CONFLICT (user_id, story_id)
    DO NOTHING
    """)
    db.session.execute(sql, {"user_id":user_id, "story_id":story_id})
    db.session.commit()
    return True

def remove_starred(id):
    user_id = users.user_id()
    if user_id == 0:
        return False

    sql = text("DELETE FROM starred WHERE starred.id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit()
    return True
