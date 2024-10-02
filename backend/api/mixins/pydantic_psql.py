from copy import deepcopy

from pydantic import BaseModel
from sqlalchemy import desc, exc, func
import sqlite3


class BaseCrud(BaseModel):
    """
    __model_kls__: Define the main postgres model to be used for the orm.

        Example:
        class SomeSerializer(BaseCrud):
            __model_kls__ = SomeSqlAlchemyModel
    """
    __db_session__ = None
    __by_alias_global__: bool = False
    __model_kls__ = None
    # __related_kls__: dict = dict(
    #     one_to_one=dict(),
    #     one_to_many=dict(),
    #     many_to_many=dict(),
    # )
    __serialize_when_none__: bool = False

    def _commit_to_database(self):
        """A shared function to make a
           commit to the database and
           handle exceptions if encountered.
        """
        try:
            self.__db_session__.commit()
        except AssertionError as err:
            self.__db_session__.rollback()
        except (exc.IntegrityError, sqlite3.IntegrityError) as err:
            self.__db_session__.rollback()
        except Exception as err:
            self.__db_session__.rollback()

    def _get_one(self, model_kls, kwargs: dict):
        """Given model class and parameters fetch data from db."""
        return self.__db_session__().query(model_kls).filter_by(
            **kwargs).first()

    def _get_many(self, model_kls, kwarg_list):
        """Assume list of kwargs need to be equal to column value."""
        objs: list = list()
        session = self.__db_session__()
        for kwarg in kwarg_list:
            objs.extend(session.query(model_kls).filter_by(**kwarg).all())
        return objs

    def _get_validated_data(self):
        pydantic_kw: dict = dict(exclude_unset=True)
        if self.__serialize_when_none__:
            pydantic_kw.update(dict(exclude_none=False, exclude_unset=False))
        if self.__by_alias_global__:
            pydantic_kw.update(dict(by_alias=True))
        return self.model_dump(**pydantic_kw)

    def update(self, filter_fields, **kwargs):
        """Provide fields/data to target the correct obj, preferable
        the id of obj.

        This update version can only handle 1-level deep updates.
        """
        # Need to handle if error occurs
        obj = self.__model_kls__.query.filter_by(
            **filter_fields).first()

        if not obj:
            return {
                'message': f'Object {self.__model_kls__} '
                           f'- {filter_fields} does exist.'
            }

        validated_data = self._get_validated_data()
        for k, v in validated_data.items():
            if not isinstance(v, (dict, list, tuple,)):
                setattr(obj, k, v)

        self.__db_session__.add(obj)
        self._commit_to_database()
        return self.return_results(obj, **kwargs)

    def create(self, **kwargs):
        """Create new row under target model."""

        # Need to handle if error occurs
        validated_data = self._get_validated_data()
        if not validated_data:
            return None

        if "id" in validated_data:
            del validated_data["id"]

        obj_created = self.__model_kls__(**validated_data)
        self.__db_session__.add(obj_created)
        self._commit_to_database()

        return self.return_results(obj_created, **kwargs)

    def get_or_create(self, **kwargs):
        if not self.__model_kls__:
            return {}
        obj = self.get_obj(**kwargs)

        if obj:
            return obj

        return self.create(**kwargs)

    def get_obj(self, **kwargs):
        """
        columns: A list of columns to pull from database and not getting
                the whole row.
                It's preferred to always include the id with the columns.
                E.g: ["id", "columns1", "columns2"]
        """
        if not self.__model_kls__:
            return {}

        data = self._get_validated_data()

        q = self.__model_kls__.query

        if data.get("id"):
            obj = q.filter_by(id=data["id"]).first()
            return self.return_results(obj, **kwargs)

        obj = q.filter_by(**data).first()

        return self.return_results(obj, **kwargs)

    def get_objs_by_order(self, order_by: dict, **kwargs):
        """
        Given model class and parameters fetch data from db.
        order_by = {desc: True/False, field: name of field to order_by}
        columns: A list of columns to pull from database and not getting the
                whole row.
                It's preferred to always include the id with the columns.
                E.g: ["id", "columns1", "columns2"]
        """

        data = self._get_validated_data()
        q = self.__model_kls__.query.filter_by(**data)

        if order_by.get("desc"):
            obj = q.order_by(desc(order_by["field"])).all()
        else:
            obj = q.order_by(order_by["field"]).all()

        return self.return_results(obj, **kwargs)

    def get_objects(self, **kwargs):
        """
        columns: A list of columns to pull from database and not getting the
                whole row.
                It's preferred to always include the id with the columns.
                E.g: ["id", "columns1", "columns2"]
        count: A boolean that will count the matching rows in db.
                count overrules any other parameters.
        """
        # TODO: need to add support for order_by
        data = self._get_validated_data()

        if kwargs.get("count") is True:
            results = self.__model_kls__.query(
                func.count(self.__model_kls__.id)).filter_by(**data).one()[0]
            return results[0] if results else 0

        results = self.__model_kls__.query.filter_by(**data).all()
        return self.return_results(results, **kwargs)

    def hard_delete(self):
        data = self._get_validated_data()

        if self.get_obj():
            self.__model_kls__.query.filter_by(id=data["id"]).delete()
            self._commit_to_database()
            return {'success': True}
        return {'message': 'Object not found.'}

    @staticmethod
    def return_results(results, **kwargs):
        if not results:
            return results

        include_hybrid = kwargs.get("include_hybrid", False)
        rel = kwargs.get("rel", False)
        return_dict = kwargs.get("return_dict", True)
        if not return_dict:
            return results

        if isinstance(results, list) and not kwargs.get("columns"):
            return [
                result.to_json(include_hybrid=include_hybrid, rel=rel)
                for result in results
            ]
        elif kwargs.get("columns"):
            if isinstance(results, list):
                return [
                    dict(zip(kwargs.get("columns"), result))
                    for result in results
                ]
            # Looses the relationship data pull if columns is specified
            return dict(zip(kwargs.get("columns"), results))

        return results.to_json(include_hybrid=include_hybrid, rel=rel)
