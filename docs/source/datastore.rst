Using Mongo or other data store
-------------------------------
Using any data store as easy as implementing all the methods from **ModelMixin**


.. code::

       from flask_error import ModelMixin
       class CustomModel(ModelMixin):
            objects = {}

            @classmethod
            def delete(cls, rhash):
                cls.objects.pop(rhash)

            @classmethod
            def create_or_update(cls, rhash, host, path, method, request_data, exception):
                count = 1
                now = datetime.datetime.now()
                created_on = now
                exception = exception

                if rhash in cls.objects:
                    error = cls.objects[rhash]
                    created_on = error.created_on
                    exception = error.exception
                    count = error.count + 1
                error = Error(rhash, host, path, method, str(request_data),
                              exception, count, created_on, now)
                cls.objects[rhash] = error

            @classmethod
            def get_all(cls):
                return cls.objects.values()

            @classmethod
            def get(cls, rhash):
                error = cls.objects.get(rhash, None)
                return error


       # create app with our own model
       error_manager = AppErrorManager(app=app, model=CustomModel)

