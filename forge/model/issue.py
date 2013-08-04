#!/usr/bin/env python
# -*- coding: utf-8 -*-

from forge import model

from sqlalchemy import (
        Column, ForeignKey, Table,
        Integer, String, Text, Boolean,
        )
from sqlalchemy.orm import relationship

from datetime import datetime


class IssueType(model.Base):
    __tablename__ = "tracker_types"
    id = Column(Integer, primary_key=True)
    value = Column(Enum("Feature", "Enhancement", "Support",
        "Epic", "User Story", "Bug", "Task"))


class Status(model.Base):
    __tablename__ = "tracker_status"
    id = Column(Integer, primary_key=True)
    value = Column(Enum("Unconfirmed", "Pending",
        "In Progress", "Resolved", "Verified", "Integrated",
        "Closed"))


class Workflow(model.Base):
    __tablename__ = "tracker_status_workflow"
    id = Column(Integer, primary_key=True)

    source_id = Column(ForeignKey("tracker_status.id"),
            nullable=True)
    source = relationship("Status", foreign_keys=[source_id])
    destination_id = Column(ForeignKey("tracker_status.id"))
    destination = relationship("Status", foreign_keys=[destination_id])
    module_id = Column(ForeignKey("modules.id"),
            nullable=True)
    module = relationship("Module")
    issue_type_id = Column(ForeignKey("tracker_types.id"),
            nullable=True)
    issue_type = relationship("IssueType")
    is_closed = Column(Boolean, default=False)


class Priority(model.Base):
    __tablename__ = "tracker_priorities"
    id = Column(Integer, primary_key=True)
    value = Column(Enum("Low", "Medium", "High", "Critical"))


class Issue(model.Base):
    __tablename__ = "tracker_issues"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    module_id = Column(ForeignKey("project_modules.id"))
    module = relationship("Project", backref="modules")
    type_id = Column(ForeignKey("tracker_types.id"))
    type = relationship("IssueType")

    creation = Column(DateTime(timezone=True),
            default=datetime.now)
    reporter_id = Column(ForeignKey("user_profiles.id"))
    reporter = relationship("User", foreign_keys=[reporter_id])
    assigned_id = Column(ForeignKey("user_profiles.id"),
            nullable=True)
    assigned = relationship("User", foreign_keys=[assigned_id])

    status_id = Column(ForeignKey("tracker_status.id"))
    status = relationship("Status")
    priority_id = Column(ForeignKey("tracker_priority.id"))
    priority = relationship("Priority")
    milestone_id = Column(ForeignKey("project_versions.id"))
    milestone = relationship("Version")


class Dependency(model.Base):
    __tablename__ = 'dependencies'
    source_id = Column(ForeignKey('issues.id'),
            primary_key=True)
    source = relationship('Issue', foreign_keys=[from_id],
            backref='dependencies')

    to_id = Column(ForeignKey('issues.id'),
            primary_key=True)
    to = relationship('Issue', foreign_keys=[to_id],
            backref='references')

    type = Column(Enum("Blocks", "Sub-Task", "Duplicate"))
