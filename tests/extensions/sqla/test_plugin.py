#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试插件中的sa辅助函数
"""
import pyperclip
import pytest

from smorest_sfs.plugins.sa.helpers import QueryAnalysis
from smorest_sfs.plugins.sa import execute, debug_sql, render_limit_results
from tests._utils.uniqueue import UniqueQueue
from tests.extensions.sqla.test_sqla import ItemsFixtureBase


class TestSAPlugin(ItemsFixtureBase):
    fixture_names = ("TestCRUDTable", "TestSASql")
    raw_sql = (
        "SELECT sqla_test_crud_table.name "
        "\nFROM sqla_test_crud_table"
        " \nWHERE sqla_test_crud_table.name = '{name}'"
    )
    table_str = "╒════════╕\n" "│ name   │\n" "╞════════╡\n" "│ bbc    │\n" "╘════════╛"

    @pytest.mark.usefixtures("TestTableTeardown", "crud_items")
    @pytest.mark.parametrize("name, count", [("bbc", 1), ("aac", 0)])
    def test_sql_could_run(self, name, count):
        data = execute(self.TestSASql, name=name)
        assert len(data) == count

    @pytest.mark.parametrize("name", ["bbc", "aac"])
    def test_raw_sql_should_rendered(self, name):
        test_sql = self.TestSASql(name)
        assert test_sql.get_raw_sql() == self.raw_sql.format(name=name)

    @pytest.mark.usefixtures("TestTableTeardown", "crud_items", "inject_logger")
    def test_table_should_rendered(self):
        render_limit_results(self.TestSASql, "bbc")
        assert self._get_debug() == "\n" + self.table_str

    @pytest.mark.usefixtures("TestTableTeardown", "crud_items", "inject_logger")
    def test_debug_should_rendered(self):
        debug_sql(self.TestSASql, "bbc")
        assert self._get_debug() == "\n" + self.raw_sql.format(
            name="bbc"
        ) and pyperclip.paste() == self.raw_sql.format(name="bbc")

    def _get_debug(self):
        queue = UniqueQueue()
        return queue.get(timeout=1)


class TestTableQuery(ItemsFixtureBase):
    fixture_names = (
        "TestCRUDTable",
        "TestSASql",
        "TestChildTable",
        "TestOneTableQuery",
        "TestOneColQuery",
        "TestTwoTablesQuery",
    )

    @pytest.mark.usefixtures("TestTableTeardown", "crud_items")
    def test_query_could_run(self):
        data = execute(self.TestOneColQuery)
        assert len(data) > 0

    @pytest.mark.usefixtures("TestTableTeardown", "crud_items", "inject_logger")
    def test_one_col_query_debug_sql(self):
        debug_sql(self.TestOneColQuery)
        assert self._get_debug() == (
            "\n"
            "SELECT sqla_test_crud_table.name \n"
            "FROM sqla_test_crud_table \n"
            "WHERE sqla_test_crud_table.name = 'bbc'"
        )

    @pytest.mark.usefixtures("TestTableTeardown", "crud_items", "inject_logger")
    def test_one_col_query_render(self):
        render_limit_results(self.TestOneColQuery)
        assert self._get_debug() == (
            "\n╒════════╕\n│ name   │\n╞════════╡\n│ bbc    │\n╘════════╛"
        )

    @pytest.mark.usefixtures("TestTableTeardown", "crud_items", "inject_logger")
    def test_one_table_query_debug_sql(self):
        debug_sql(self.TestOneTableQuery)
        assert self._get_debug() == (
            "\n"
            "SELECT sqla_test_crud_table.id, sqla_test_crud_table.deleted, "
            "sqla_test_crud_table.modified, sqla_test_crud_table.created, "
            "sqla_test_crud_table.name \n"
            "FROM sqla_test_crud_table \n"
            "WHERE sqla_test_crud_table.deleted = false AND sqla_test_crud_table.name = "
            "'bbc'"
        )

    @pytest.mark.usefixtures("TestTableTeardown", "crud_items", "inject_logger")
    def test_one_table_query_render(self):
        render_limit_results(self.TestOneTableQuery)
        assert self._get_debug() == (
            "\n"
            "╒══════╤═══════════╤═════════════════════╤═════════════════════╤════════╕\n"
            "│   id │ deleted   │ modified            │ created             │ name   │\n"
            "╞══════╪═══════════╪═════════════════════╪═════════════════════╪════════╡\n"
            "│    4 │ False     │ 1994-09-11 08:20:00 │ 1994-09-11 08:20:00 │ bbc    │\n"
            "╘══════╧═══════════╧═════════════════════╧═════════════════════╧════════╛"
        )

    @pytest.mark.usefixtures(
        "TestTableTeardown", "crud_items", "inject_logger", "child_items"
    )
    def test_two_tables_query_debug_sql(self):
        debug_sql(self.TestTwoTablesQuery)
        assert self._get_debug() == (
            "\n"
            "SELECT sqla_test_crud_table.id, sqla_test_crud_table.deleted, "
            "sqla_test_crud_table.modified, sqla_test_crud_table.created, "
            "sqla_test_crud_table.name, test_crud_child_table.id, "
            "test_crud_child_table.deleted, test_crud_child_table.modified, "
            "test_crud_child_table.created, test_crud_child_table.name, "
            "test_crud_child_table.pid, sqla_test_crud_table.id AS crud_id \n"
            "FROM sqla_test_crud_table, test_crud_child_table \n"
            "WHERE sqla_test_crud_table.name = 'bbc'"
        )

    @pytest.mark.usefixtures(
        "TestTableTeardown", "crud_items", "inject_logger", "child_items"
    )
    def test_two_tables_query_render(self):
        render_limit_results(self.TestTwoTablesQuery)
        assert self._get_debug() == (
            "\n"
            "╒═══════════════════╤═══════════════════"
            "═╤══════════╤════════╤═══════════╕\n"
            "│ TestCRUDTable     │ TestChildTable    "
            " │ name     │ name   │   crud_id │\n"
            "╞═══════════════════╪═══════════════════"
            "═╪══════════╪════════╪═══════════╡\n"
            "│ <TestCRUDTable 4> │ <TestChildTable 1>"
            " │ aaabbb   │ bbc    │         4 │\n"
            "├───────────────────┼───────────────────"
            "─┼──────────┼────────┼───────────┤\n"
            "│ <TestCRUDTable 4> │ <TestChildTable 2>"
            " │ bbbbcccc │ bbc    │         4 │\n"
            "├───────────────────┼───────────────────"
            "─┼──────────┼────────┼───────────┤\n"
            "│ <TestCRUDTable 4> │ <TestChildTable 3>"
            " │ bbcccc   │ bbc    │         4 │\n"
            "├───────────────────┼───────────────────"
            "─┼──────────┼────────┼───────────┤\n"
            "│ <TestCRUDTable 4> │ <TestChildTable 4>"
            " │ bbc      │ bbc    │         4 │\n"
            "╘═══════════════════╧═══════════════════"
            "═╧══════════╧════════╧═══════════╛"
        )

    def _get_debug(self):
        queue = UniqueQueue()
        return queue.get(timeout=1)
