#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from typing import Union

import pendulum


def utcnow() -> datetime.datetime:
    return datetime.datetime.utcnow()


def _utctoday(now: datetime.datetime) -> datetime.date:
    return now.date()


def utctoday() -> datetime.date:
    now = datetime.datetime.utcnow()
    return _utctoday(now)


def convert_timezone(
    dt: Union[pendulum.datetime, datetime.datetime], timezone: str
) -> pendulum.datetime:
    tz = pendulum.timezone(timezone)
    return tz.convert(dt)
