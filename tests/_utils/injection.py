#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List, Tuple, Type, Union

from flask import url_for
from marshmallow import Schema

import pytest
from smorest_sfs.extensions.sqla import Model

from .uniqueue import UniqueQueue


def log_to_queue(record):
    queue = UniqueQueue()
    queue.put(record.record["message"])
    return record


def inject_logger(logger):
    logger.add(log_to_queue, serialize=False)


def uninject_logger(logger):
    logger.remove()


class FixturesInjectBase:

    items: str
    listview: str
    view: str
    item_view: str
    login_roles: List[str]
    model: Type[Model]
    schema: Type[Schema]
    delete_param_key: str
    fixture_names: Union[Tuple[str], Tuple] = ()

    @pytest.fixture(autouse=True)
    def auto_injector_fixture(self, request):
        names = self.fixture_names
        for name in names:
            setattr(self, name, request.getfixturevalue(name))


class GeneralModify(FixturesInjectBase):
    def _add_request(self, data):
        with self.flask_app_client.login(self.regular_user, self.login_roles) as client:
            with self.flask_app.test_request_context():
                url = url_for(self.view)
                resp = client.post(url, json=data)
                self.model.query.filter_by(id=resp.json["data"]["id"]).delete()
                self.db.session.commit()
                return resp

    def _get_deleting_items(self):
        items = getattr(self, self.items)
        return items[:1]

    def _get_modified_item(self):
        items = getattr(self, self.items)
        return items[-1]

    @staticmethod
    def __get_schema_dumped(schema, item):
        return schema.dump(item)

    def _get_dumped_modified_item(self):
        item = self._get_modified_item()
        schema = self.schema()
        return self.__get_schema_dumped(schema, item)

    def _delete_request(self):
        with self.flask_app_client.login(self.regular_user, self.login_roles) as client:
            with self.flask_app.test_request_context():
                url = url_for(self.view)
                items = self._get_deleting_items()
                ids = [i.id for i in items]
                resp = client.delete(url, json={"lst": ids})
                return resp, items

    def _item_modify_request(self, json):
        with self.flask_app_client.login(self.regular_user, self.login_roles) as client:
            with self.flask_app.test_request_context():
                item = self._get_modified_item()
                url = url_for(self.item_view, **{self.delete_param_key: item.id})
                return client.put(url, json=json)

    def _item_delete_request(self):
        with self.flask_app_client.login(self.regular_user, self.login_roles) as client:
            with self.flask_app.test_request_context():
                item = self._get_modified_item()
                url = url_for(self.item_view, **{self.delete_param_key: item.id})
                resp = client.delete(url)
                return resp, item


class GeneralGet(FixturesInjectBase):
    def _get_view(self, endpoint: str, **kwargs):
        with self.flask_app_client.login(self.regular_user, self.login_roles) as client:
            with self.flask_app.test_request_context():
                url = url_for(endpoint, **kwargs)
                return client.get(url)

    def _get_option(self):
        resp = self._get_view(self.listview)
        assert (
            resp.status_code == 200
            and isinstance(resp.json["data"], list)
            and resp.json["data"][0].keys() == {"id", "name"}
        )

    def _get_list(self, **kwargs):
        resp = self._get_view(self.view, **kwargs)
        assert resp.status_code == 200 and isinstance(resp.json["data"], list)
        return resp.json["data"]

    def _get_item(self, **kwargs):
        resp = self._get_view(self.item_view, **kwargs)
        assert resp.status_code == 200 and isinstance(resp.json["data"], dict)
        return resp.json["data"]
