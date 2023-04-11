from db import db
from sqlalchemy import text
import users, stories

def get_votes_by_story(story_id):
    sql = text("""
    SELECT sum(vote)
    FROM votes WHERE story_id=:story_id
    """)
    result = db.session.execute(sql, {"story_id":story_id})
    return result.fetchone()

def get_votes_by_user(user_id):
    sql = text("""
    SELECT *
    FROM stories
    WHERE user_id=:user_id
    """)
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def get_vote_count_by_story(story_id):
    sql = text("""
    SELECT count(*)
    FROM stories
    WHERE story_id=:story_id
    """)
    result = db.session.execute(sql, {"story_id":story_id})
    return result.fetchone()

def add_upvote(story_id):
    user_id = users.user_id()
    if user_id == 0:
        return False

    sql = text("""
    INSERT INTO votes (user_id, story_id, vote)
    VALUES (:user_id, :story_id, 1)
    ON CONFLICT (user_id, story_id)
    DO UPDATE SET vote=1
    """)
    db.session.execute(sql, {"user_id":user_id,
                             "story_id":story_id})
    db.session.commit()

    return True

def add_downvote(story_id):
    user_id = users.user_id()
    if user_id == 0:
        return False

    sql = text("""
    INSERT INTO votes (user_id, story_id, vote)
    VALUES (:user_id, :story_id, -1)
    ON CONFLICT (user_id, story_id)
    DO UPDATE SET vote=-1
    """)
    db.session.execute(sql, {"user_id":user_id,
                             "story_id":story_id})
    db.session.commit()

    return True

def remove_vote(story_id):
    user_id = users.user_id()
    if user_id == 0:
        return False

    sql = text("""
    DELETE FROM votes
    WHERE votes.user_id=:user_id
    AND votes.story_id=:story_id
    """)
    db.session.execute(sql, {"user_id":user_id,
                             "story_id":story_id})
    db.session.commit()
    return True
