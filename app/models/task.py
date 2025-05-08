from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text, DateTime
from datetime import datetime
from ..db import db

class Task(db.Model):
    # So SQLAlchemy handle the table vs. manually
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


    # def to_dict(self):
    #     task_as_dict = {}
    #     task_as_dict["id"] = self.id
    #     task_as_dict["title"] = self.title
    #     task_as_dict["description"] = self.description
    #     task_as_dict["completed_at"] = self.completed_at if self.completed_at else None 
    #     return task_as_dict
    #     # check last attr later for converting ISO to datetime
    
    def to_dict(self):

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": bool(self.completed_at)
        }


    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title=task_data["title"],
            description=task_data["description"],
            completed_at=task_data.get("completed_at")  
        )    

    def update_from_dict(self, task_data):
        if "title" in task_data:
            self.title = task_data["title"]
        if "description" in task_data:
            self.description = task_data["description"]
        if "completed_at" in task_data:
            self.completed_at = task_data["completed_at"]