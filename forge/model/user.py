#!/usr/bin/env python
# -*- coding: utf-8 -*-

from forge import model

from sqlalchemy import (
        Column, ForeignKey, Table,
        Integer, String,
        Boolean,
        )
from sqlalchemy.orm import relationship


class User(model.Base):
    __tablename__ = "user_profiles"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    email = Column(String)


class Group(model.Base):
    __tablename__ = "user_groups"
    id = Column(Integer, primary_key=True)
    name = Column(String)


assignment_permissions = Table("user_assignment_permissions",
        model.Base.metadata,
        Column("assignment", ForeignKey("user_assignments.id")),
        Column("permission", ForeignKey("user_permissions.id")),
        )


class Assignment(model.Base):
    __tablename__ = "user_assignments"
    id = Column(Integer, primary_key=True)
    role_id = Column(ForeignKey("user_roles.id"))
    role = relationship("Role")
    module_id = Column(ForeignKey("project_modules.id"),
            nullable=True)
    module = relationship("Module")
    inherit_module = Column(Boolean, nullable=True)
    type = Column(String, nullable=True)
    __mapper_args__ = {
            'polymorphic_on' : type,
            'polymorphic_identity' : None,
            }
    permissions = relationship("Permission",
            secondary=assignment_permissions)


class UserAssignment(Assignment):
    user_id = Column(ForeignKey("user_profiles.id"))
    user = relationship("User")
    __mapper_args__ = {
            'polymorphic_identity' : 'user',
            }


class GroupAssignment(Assignment):
    group_id = Column(ForeignKey("user_groups.id"))
    group = relationship("Group")
    __mapper_args__ = {
            'polymorphic_identity' : 'group',
            }


subroles = Table("user_subroles", model.Base.metadata,
        Column("role_id", ForeignKey("user_roles.id"),
            primary_key=True),
        Column("subrole_id", ForeignKey("user_roles.id"),
            primary_key=True),
        )


class Role(model.Base):
    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    active = Boolean
    subroles = relationship("Role",
            secondary=subroles,
            primaryjoin=id==subroles.c.role_id,
            secondaryjoin=id==subroles.c.subrole_id,
            backref="superoles")


class Permission(model.Base):
    __tablename__ = "user_permissions"
    id = Column(Integer, primary_key=True)
    action = Column(String)
    target = Column(String)
