#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import datetime

from freezegun import freeze_time

import pendulum
from smorest_sfs.utils.datetime import utcnow, utctoday, convert_timezone

FREEZETIME = "1994-09-11 08:20:00"


@freeze_time(FREEZETIME)
def test_utcnow():
    now = utcnow()

    assert str(now) == FREEZETIME


@freeze_time(FREEZETIME)
def test_utctoday():
    today = utctoday()

    assert str(today) == "1994-09-11"


@freeze_time(FREEZETIME)
def test_convert_timezone_for_pendulum():
    pendulum_dt = pendulum.now("utc")
    sh_dt = convert_timezone(pendulum_dt, "Asia/Shanghai")
    assert sh_dt.to_datetime_string() == "1994-09-11 16:20:00"
