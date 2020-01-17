"""测试sqla"""

import pytest
from marshmallow import Schema, fields
from sqlalchemy.exc import ProgrammingError
from werkzeug.exceptions import NotFound
from app.extensions.sqla import Model, SurrogatePK


class TestSqla:
    def test_soft_delete(self, app, db):
        class SoftDelete(Model):
            id = db.Column(db.Integer, primary_key=True)
            deleted = db.Column(db.Boolean, default=False)

        for _ in range(10):
            last = SoftDelete.create()

        assert SoftDelete.query.count() == 10
        last.delete()
        assert SoftDelete.query.count() == 9
        item = SoftDelete.query.with_deleted().get(last.id)
        assert item is not None
        assert SoftDelete.query.with_deleted().count() == 10

    def test_filter_like_by(self, app, db):
        class FilterLikeBy(Model):
            id = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String(50))
            deleted = db.Column(db.Boolean, default=False)

        try:
            FilterLikeBy.__table__.create(db.get_engine())
        except ProgrammingError:
            pass
        FilterLikeBy.create(name="aaaabbbb")
        FilterLikeBy.create(name="bbbbcccc")
        FilterLikeBy.create(name="bbcccc")
        FilterLikeBy.create(name="bbc")
        cnt = FilterLikeBy.query.filter_like_by(name="bc").count()
        assert cnt == 3

    def test_surrogate_pk(self, app, db):
        class TestPk(SurrogatePK):

            name = db.Column(db.String(1))

        for key in ["id", "deleted", "modified", "created"]:
            assert hasattr(TestPk, key)

    def test_base_crud(self, app, db):
        class TestBaseCRUD(Model, SurrogatePK):
            name = db.Column(db.String(4))

        class TestSchema(Schema):
            name = fields.Str()

        try:
            TestBaseCRUD.__table__.create(db.get_engine())
        except ProgrammingError:
            pass

        cruds = [TestBaseCRUD.create(name=str(i)) for i in range(10)]

        item = TestBaseCRUD.get_by_id(cruds[0].id)
        assert item is cruds[0]
        TestBaseCRUD.update_by_id(
            item.id, TestSchema, TestBaseCRUD(name="111")
        )
        item = TestBaseCRUD.get_by_id(cruds[0].id)
        assert item.name == "111"
        TestBaseCRUD.delete_by_id(item.id)
        with pytest.raises(NotFound):
            item = TestBaseCRUD.get_by_id(cruds[0].id)
        TestBaseCRUD.delete_by_ids([i.id for i in cruds[1:6]])
        assert TestBaseCRUD.query.count() == 4
