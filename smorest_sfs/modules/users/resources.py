#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    app.modules.users.resource
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    用户的资源模块
"""
from typing import Dict, List

from flask.views import MethodView
from flask_sqlalchemy import BaseQuery
from loguru import logger

from flask_jwt_extended import current_user
from smorest_sfs.extensions import db
from smorest_sfs.extensions.api.decorators import paginate
from smorest_sfs.extensions.marshal.bases import (BaseIntListSchema,
                                                  BaseMsgSchema,
                                                  GeneralLikeArgs)
from smorest_sfs.modules.auth import PERMISSIONS, ROLES
from smorest_sfs.modules.auth.decorators import (doc_login_required,
                                                 permission_required,
                                                 role_required)
from smorest_sfs.services.users import create_user

from . import blp, models, schemas


@blp.route("/options")
class UserListView(MethodView):
    @doc_login_required
    @permission_required(PERMISSIONS.UserQuery)
    @blp.response(schemas.UserListSchema)
    def get(self) -> Dict[str, List[models.User]]:
        # pylint: disable=unused-argument
        """
        获取所有用户选项信息
        """
        query = models.User.query

        items = query.all()

        return {"data": items}


@blp.route("")
class UserView(MethodView):
    @doc_login_required
    @permission_required(PERMISSIONS.UserQuery)
    @blp.arguments(GeneralLikeArgs, location="query", as_kwargs=True)
    @blp.response(schemas.UserPageSchema)
    @paginate()
    def get(self, name) -> BaseQuery:
        # pylint: disable=unused-argument
        """
        获取所有用户信息——分页
        """
        query = models.User.query.join(models.User.userinfo)
        if name:
            like_key = "%{}%".format(name)
            query = query.filter(
                db.or_(
                    models.UserInfo.last_name.like(like_key),
                    models.UserInfo.first_name.like(like_key),
                    models.User.username.like(like_key),
                    (models.UserInfo.first_name + models.UserInfo.last_name).like(
                        like_key
                    ),
                )
            )

        return query

    @doc_login_required
    @permission_required(PERMISSIONS.UserDelete)
    @blp.arguments(BaseIntListSchema, as_kwargs=True)
    @blp.response(BaseMsgSchema)
    def delete(self, lst: List[int]):
        # pylint: disable=unused-argument
        """
        批量删除用户
        -------------------------------
        :param lst: list 包含id列表的字典
        """

        models.User.delete_by_ids(lst)
        logger.info(f"{current_user.username}删除了用户{lst}")


@blp.route(
    "/<int:user_id>",
    parameters=[{"in": "path", "name": "user_id", "description": "用户id"}],
)
class UserItemView(MethodView):
    @doc_login_required
    @permission_required(PERMISSIONS.UserEdit)
    @blp.arguments(schemas.UserSchema)
    @blp.response(schemas.UserItemSchema)
    def put(self, user: models.User, user_id: int) -> Dict[str, models.User]:
        """
        更新用户
        """
        user = models.User.update_by_id(user_id, schemas.UserSchema, user)
        logger.info(f"{current_user.username}更新了用户{user.id}")

        return {"data": user}

    @doc_login_required
    @permission_required(PERMISSIONS.UserDelete)
    @blp.response(BaseMsgSchema)
    def delete(self, user_id: int):
        """
        删除用户
        """
        models.User.delete_by_id(user_id)
        logger.info(f"{current_user.username}删除了用户{user_id}")

    @doc_login_required
    @permission_required(PERMISSIONS.UserQuery)
    @blp.response(schemas.UserItemSchema)
    def get(self, user_id: int) -> Dict[str, models.User]:
        """
        获取单条用户
        """
        user = models.User.get_by_id(user_id)

        return {"data": user}


@blp.route("/register")
class UserRegisterView(MethodView):
    @blp.arguments(schemas.UserSchema)
    @blp.response(schemas.UserItemSchema)
    def put(self, user: models.User) -> Dict[str, models.User]:
        user = create_user(user)
        return {"data": user}


@blp.route("/userinfo")
class UserSelfView(MethodView):
    @doc_login_required
    @role_required(ROLES.User)
    @blp.response(schemas.UserItemSchema, description="用户信息")
    def get(self):
        """
        获取用户自己的信息
        """

        return {"data": current_user}

    @doc_login_required
    @role_required(ROLES.User)
    @blp.arguments(schemas.UserSelfSchema)
    @blp.response(schemas.UserItemSchema, code=200, description="用户信息")
    def patch(self, user: models.User):
        """
        更新用户信息
        """
        models.User.update_by_id(
            current_user.id, schemas.UserSelfSchema, user
        )
        logger.info(f"{current_user.username}更新了个人信息")

        return {"data": current_user}
