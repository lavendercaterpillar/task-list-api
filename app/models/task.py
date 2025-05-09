from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from typing import Optional
from datetime import datetime
from ..db import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .goal import Goal

class Task(db.Model):
    # So SQLAlchemy handle the table vs. manually
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")


    def to_dict(self):
        task_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": bool(self.completed_at)
        }

        if self.goal_id:
            task_dict["goal_id"] = self.goal_id

        return task_dict
    #     # check last attr later for converting between ISO & datetime
    
    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         "title": self.title,
    #         "description": self.description,
    #         "is_complete": bool(self.completed_at)
    #     }


    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title=task_data["title"],
            description=task_data["description"],
            completed_at=task_data.get("completed_at"),
            goal_id=task_data.get("goal_id")
        )    

    def update_from_dict(self, task_data):
        if "title" in task_data:
            self.title = task_data["title"]
        if "description" in task_data:
            self.description = task_data["description"]
        if "completed_at" in task_data:
            self.completed_at = task_data["completed_at"]
        if "goal_id" in task_data:
            self.goal_id = task_data["goal_id"]