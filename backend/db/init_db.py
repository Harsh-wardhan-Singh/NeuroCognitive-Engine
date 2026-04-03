from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from db.database import Base, engine
from db.models import Attempt, MasteryState, Session, SessionQuestion, User
MODEL_TABLES = [
	User.__table__,
	Attempt.__table__,
	MasteryState.__table__,
	Session.__table__,
	SessionQuestion.__table__,
]
def init_db():
	Base.metadata.create_all(bind=engine, tables=MODEL_TABLES)
if __name__ == "__main__":
	init_db()