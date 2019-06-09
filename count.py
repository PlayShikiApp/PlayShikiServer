from sqlalchemy import func
from shikimori import app
from shikimori import models
print(app.db.session.query(func.count(models.AnimeVideo.id)).scalar())
