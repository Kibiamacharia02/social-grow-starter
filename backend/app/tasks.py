from celery import Celery
import os
from .db import SessionLocal
from .models import Post, Account
from .instagram_api import create_media_container, publish_media
from .utils import decrypt_token
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

CELERY_BROKER = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/1")

cel = Celery("tasks", broker=CELERY_BROKER, backend=CELERY_BACKEND)

@cel.task(bind=True, max_retries=3)
def publish_post(self, post_id: int):
    db = SessionLocal()
    try:
        post = db.query(Post).filter(Post.id==post_id).first()
        if not post:
            return
        account = db.query(Account).filter(Account.id==post.account_id).first()
        if not account:
            post.status = "failed"; db.commit(); return
        access_token = decrypt_token(account.access_token)
        ig_user_id = account.platform_user_id
        container_id = create_media_container(ig_user_id, post.media_url, post.content, access_token)
        resp = publish_media(ig_user_id, container_id, access_token)
        post.platform_post_id = resp.get("id")
        post.status = "published"
        post.published_at = datetime.utcnow()
        db.commit()
    except Exception as e:
        db.rollback()
        try:
            self.retry(exc=e, countdown=60*(self.request.retries+1))
        except self.MaxRetriesExceededError:
            p = db.query(Post).filter(Post.id==post_id).first()
            if p:
                p.status = "failed"
                db.commit()
    finally:
        db.close()
