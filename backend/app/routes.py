from fastapi import APIRouter, Depends, HTTPException
from .schemas import PostCreate, PostOut
from .db import SessionLocal
from . import models, tasks
from sqlalchemy.orm import Session

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/posts/", response_model=PostOut)
def create_post(req: PostCreate, db: Session = Depends(get_db)):
    p = models.Post(
        account_id=req.account_id,
        content=req.content,
        media_url=req.media_url,
        scheduled_at=req.scheduled_at,
        status="scheduled"
    )
    db.add(p); db.commit(); db.refresh(p)
    eta = req.scheduled_at
    tasks.publish_post.apply_async(args=[p.id], eta=eta)
    return p

@router.get("/posts/", response_model=list[PostOut])
def list_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).order_by(models.Post.scheduled_at.desc()).all()

@router.post("/posts/{post_id}/publish-now")
def publish_now(post_id: int, db: Session = Depends(get_db)):
    p = db.query(models.Post).filter(models.Post.id==post_id).first()
    if not p:
        raise HTTPException(404, "Not found")
    tasks.publish_post.delay(p.id)
    return {"status":"queued"}
