Masking Rule
-------------

- Disable masking rule: set :code:`APP_ERROR_MASKED_KEY_HAS = None`
- To set other mask rule add following lines

.. code::

    #Mask all the variables or dictionary keys which contains from one of the following tuple
    APP_ERROR_MASKED_KEY_HAS = ( 'secret', 'card', 'credit', 'pass' )
    #Replace value with  `###@@@@@###`
    APP_ERROR_MASK_WITH = "###@@@@@###"





.. note::
    - Masking is performed for each variable like dict, list, set and all.
    - Masking is performed on the dictionary key as well as e.g. *ImmutableMultiDict*, standard dict or any object whose super class is dict.

###################
Custom masking rule
###################

Using MaskableMixin
^^^^^^^^^^^^^^^^^^^

implement __call__ method of

.. code::

        from flask_error import MaskableMixin
        class MyMaskable(MaskableMixin):
            def __call__(self, key):
                # Put any logic
                # Do not mask return False,None
                # To mask return True, Value

        # create app as
        ...
        app = Flask(__name__)
        db = SQLAlchemy(app)
        error_manager = AppErrorManager(app=app, db=db, maskable=MyMaskable("#########", ('pass', 'card') ) )
        db.create_all()
        return app, db, error_manager
        ...


Using function
^^^^^^^^^^^^^^
.. code::

    def mask(key):
        # Put any logic
        # Do not mask return False,None
        # To mask return True, Value

    # create app as
    ...
    app = Flask(__name__)
    db = SQLAlchemy(app)
    error_manager = AppErrorManager(app=app, db=db, maskable=mask )
    db.create_all()
    return app, db, error_manager