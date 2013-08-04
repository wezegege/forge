#!/usr/bin/env python
# -*- coding: utf-8 -*-

from forge import model

from sqlalchemy import (
        Column, ForeignKey, Table,
        Integer, String,
        Boolean,
        )
from sqlalchemy.orm import relationship


class ModuleType(model.Base):
    __tablename__ = 'project_types'
    id = Column(Integer, primary_key=True)
    value = Column(Enum("Project", "Product", "Module", "Component", "Library"))


submodule = Table('project_submodules', model.Base.metadata,
        Column('module_id', ForeignKey('modules.id')),
        Column('submodule_id', ForeignKey('modules.id')),
        )


class Module(model.Base):
    __tablename__ = "project_modules"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type_id = Column(ForeignKey("project_types.id"))
    type = relationship("ModuleType")
    project_id = Column(ForeignKey("projects.id"))
    project = relationship("Project", backref="modules")
    submodules = relationship("Module", secondary=submodule,
            primaryjoin=id==submodule.c.module_id,
            secondaryjoin=id==submodule.c.submodule_id,
            backref="supermodules")


class Version(model.Base):
    __tablename__ = "project_versions"
    id = Column(Integer, primary_key=True)
    value = Column(String)
    released = Column(Boolean)
    project_id = Column(ForeignKey("project_modules.id"))
    project = relationship("Project", backref="versions")
