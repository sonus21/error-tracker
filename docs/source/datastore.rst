Using Mongo or other data store
-------------------------------
Using any data store as easy as implementing all the methods from **ModelMixin**


.. code::

       from error_tracker import ModelMixin
       class CustomModel(ModelMixin):
            objects = {}

            @classmethod
            def delete_entity(cls, rhash):
                ...

            @classmethod
            def create_or_update_entity(cls, rhash, host, path, method, request_data, exception_name, traceback):
                ...

            @classmethod
            def get_exceptions_per_page(cls, page_number=1):
                ...

            @classmethod
            def get_entity(cls, rhash):
                ...


Flask App Usage
===============
Create app with the specific model

    .. code::

       error_tracker = AppErrorTracker(app=app, model=CustomModel)

Django App Usage
================

Add path to the model in settings file as

   .. code::

        APP_ERROR_DB_MODEL = core.CustomModel
