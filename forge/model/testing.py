#!/usr/bin/env python
# -*- coding: utf-8 -*-

from forge import model

from sqlalchemy import (
        Column, ForeignKey, Table,
        Integer, String, Boolean, Text,
        )
from sqlalchemy.orm import relationship

from datetime import datetime


class TestSuite(model.Base):
    __tablename__ = 'test_suites'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    active = Column(Boolean)
    parent_id = Column(ForeignKey("test_suites.id"),
            nullable=True, backref="children")
    parent = relationship("TestSuite", backref="children")
    module_id = Column(ForeignKey("project_modules.id"),
            nullable=True)
    module = relationship("Module", backref='testsuites')


class TestCase(model.Base):
    __tablename__ = 'test_cases'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    active = Column(Boolean)
    automatic = Column(Boolean)
    description = Column(Text)
    requirements = Column(Text)
    testsuite_id = Column(ForeignKey("test_suites.id"))
    testsuite = relationship(TestSuite, backref="tests")


class Step(model.Base):
    __tablename__ = 'test_steps'
    id = Column(Integer, primary_key=True)
    testcase_id = Column(ForeignKey("test_cases.id"))
    testcase = relationship(TestCase, backref="steps")
    action = Column(Text)
    outcome = Column(Text)


testcase_to_testplan = Table("test_case_to_plan",
        model.Base.metadata,
        Column("testcase_id", ForeignKey("test_cases.id")),
        Column("testplan_id", ForeignKey("test_plans.id")),
        )


class TestPlan(model.Base):
    __tablename__ = 'testplans'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    active = Column(Boolean)
    testcases = relationship("TestCase",
            secondary=testcase_to_testplan,
            backref="testplans")


class TestCampaign(model.Base):
    __tablename__ = 'test_campaigns'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    module_id = Column(ForeignKey("project_modules.id"))
    module = relationship("Module", backref='testcampaigns')
    version_id = Column(ForeignKey("project_versions.id"),
            nullable=True)
    version = relationship("Version", backref='testcampaigns')
    testplan_id = Column(ForeignKey("test_plans.id"))
    testplan = relationship("TestPlan", backref="campaigns")


class TestRun(model.Base):
    __tablename__ = 'test_runs'
    id = Column(Integer, primary_key=True)
    testcampaign_id = Column(ForeignKey("test_campaigns.id"))
    testcampaign = relationship("TestCampaign",
            backref="testruns")
    tester_id = Column(ForeignKey("user_profiles.id"))
    tester = relationship("User")
    date = Column(Datetime, default=datetime.now)
    status = Column(Enum("Passed", "Error", "Failed"))
    comments = Column(Text)


