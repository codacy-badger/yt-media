#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from flask import url_for

from tests._utils.injection import FixturesInjectBase


class TestGeneralAccess(FixturesInjectBase):
    fixture_names = ("flask_app_client", "flask_app", "regular_user")

    @pytest.mark.parametrize(
        "http_method, view, kw",
        (
            ("GET", "Storages.StoragesView", {"file_id": 1}),
            ("DELETE", "Storages.StoragesView", {"file_id": 1}),
            ("DELETE", "Storages.ForceDeleteView", {"file_id": 1}),
        ),
    )
    def test_unauthorized_access(self, http_method, view, kw):
        with self.flask_app.test_request_context():
            url = url_for(view, **kw)
            response = self.flask_app_client.open(method=http_method, path=url)
            assert response.status_code == 401

    @pytest.mark.parametrize(
        "http_method, view, kw",
        (
            ("GET", "Storages.StoragesView", {"file_id": 1}),
            ("DELETE", "Storages.StoragesView", {"file_id": 1}),
            ("DELETE", "Storages.ForceDeleteView", {"file_id": 1}),
        ),
    )
    def test_forbbden_access(self, http_method, view, kw):
        with self.flask_app.test_request_context():
            with self.flask_app_client.login(self.regular_user, []) as client:
                url = url_for(view, **kw)
                response = client.open(method=http_method, path=url)
                assert response.status_code == 403
