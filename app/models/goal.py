from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, DateTime
from ..db import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .task import Task

class Goal(db.Model):
    # So SQLAlchemy handle the table vs. manually
    __tablename__ = "goal"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")

    def to_dict(self):

        return {
            "id": self.id,
            "title": self.title
        }


    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title=task_data["title"]
        )    

    def update_from_dict(self, task_data):
        if "title" in task_data:
            self.title = task_data["title"]
