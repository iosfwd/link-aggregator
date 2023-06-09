from db import db
from sqlalchemy import text
import users

def get_list(story_id):
    sql = text("""
    SELECT C.id, C.body, C.created_at, C.parent_comment_id,
    C.user_id, C.hidden, C.story_id, U.username
    FROM comments C, users U
    WHERE C.user_id=U.id AND C.story_id=:story_id
    """)
    result = db.session.execute(sql, {"story_id":story_id})
    return result.fetchall()

def get_comment(id):
    sql = text("""
    SELECT id, body, created_at, parent_comment_id, user_id, story_id, hidden
    FROM comments
    WHERE id=:id AND hidden = FALSE
    """)
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def send(body, user_id, story_id):
    if user_id == 0:
        return False

    sql = text("""
    INSERT INTO comments (body, user_id, story_id)
    VALUES (:body, :user_id, :story_id)
    """)
    db.session.execute(sql, {"body":body,
                             "user_id":user_id,
                             "story_id":story_id})
    db.session.commit()
    return True

def reply(body, user_id, story_id, parent_comment_id):
    if user_id == 0:
        return False

    sql = text("""
    INSERT INTO comments (body, user_id, story_id, parent_comment_id)
    VALUES (:body, :user_id, :story_id, :parent_comment_id)
    """)
    db.session.execute(sql, {"body":body,
                             "user_id":user_id,
                             "story_id":story_id,
                             "parent_comment_id":parent_comment_id})
    db.session.commit()
    return True

def edit_comment(body, comment_id):
    if users.user_id() == 0:
        return False

    sql = text("""
    UPDATE comments
    SET body=:body
    WHERE comments.id=:comment_id
    """)
    db.session.execute(sql, {"body":body,
                             "comment_id":comment_id})
    db.session.commit()
    return True

def hide_comment(comment_id):
    if users.user_id() == 0:
        return False

    sql = text("""
    UPDATE comments
    SET hidden=TRUE
    WHERE comments.id=:comment_id
    """)
    db.session.execute(sql, {"comment_id":comment_id})
    db.session.commit()
    return True
