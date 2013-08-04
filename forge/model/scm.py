#!/usr/bin/env python
# -*- coding: utf-8 -*-

from forge import model

from sqlalchemy import (
        Column, ForeignKey, Table,
        Integer, String,
        Boolean,
        )
from sqlalchemy.orm import relationship


class SCM(model.Base):
    __tablename__ = "scm_codebase"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    module_id = Column(ForeignKey("project_modules.id"))
    module = relationship("Module")


class Branch(model.Base):
    __tablename__ = 'scm_branches'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    scm_id = Column(ForeignKey("scm_codebases.id"))
    scm = relationship("SCM")


branch_commit = Table('scm_branch_commit', model.Base.metadata,
        Column('commit_id', ForeignKey('scm_commits.id')),
        Column('branch_id', ForeignKey('scm_branches.id')),
            )


class Commit(model.Base):
    __tablename__ = 'scm_commits'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    author_id = Column(ForeignKey("user_profiles.id"))
    author = relationship("User")
    scm_id = Column(ForeignKey("scm_codebases.id"))
    scm = relationship("SCM")
    branches = relationship("Branch", secondary=branch_commit,
        backref="commits")


class Tag(model.Base):
    __tablename__ = 'scm_tags'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    version_id = Column(ForeignKey("project_versions.id"),
            nullable=True)
    version = relationship("Version", backref='tag')
    scm_id = Column(ForeignKey("scm_codebases.id"))
    scm = relationship("SCM")


class SourceFile(model.Base):
    __tablename__ = 'scm_sourcefiles'
    id = Column(Integer, primary_key=True)
    path = Column(String)
    scm_id = Column(ForeignKey("scm_codebases.id"))
    scm = relationship("SCM")


class Change(model.Base):
    __tablename__ = 'scm_change'
    commit_id = Column(ForeignKey("scm_commits.id"),
            primary_key=True)
    commit = relationship("Commit", backref="changes")
    sourcefile_id = Column(ForeignKey("scm_sourcefiles.id"),
        primary_key=True)
    sourcefile = relationship("SourceFile", backref="changes")
    diff = Column(Text, nullable=True)
