Masking Rule
-------------
Masking is essential for any system so that sensitive information can't be exposed in plain text form.
Flask error monitor provides masking feature, that can be disabled or enabled.

- Disable masking rule: set :code:`APP_ERROR_MASKED_KEY_HAS = ()`
- To set other mask rule add following lines

.. code::

    #Mask all the variables or dictionary keys which contains from one of the following tuple
    APP_ERROR_MASKED_KEY_HAS = ( 'secret', 'card', 'credit', 'pass' )
    #Replace value with  `###@@@@@###`
    APP_ERROR_MASK_WITH = "###@@@@@###"


.. note::
    - Masking is performed for each variable like dict, list, set and all and it's done based on the *variable name*
    - Masking is performed on the dictionary key as well as e.g. *ImmutableMultiDict*, *QueryDict* standard dict or any object whose super class is dict.

**Custom masking rule using MaskingMixin**

.. note::
    implement __call__ method of MaskingMixin

.. code::

        from error_tracker import MaskingMixin
        class MyMaskingRule(MaskingMixin):
            def __call__(self, key):
                # Put any logic
                # Do not mask return False, None
                # To mask return True, Value



Flask App Usage
===============

.. code::

        error_tracker = AppErrorTracker(app=app, db=db,
                                         masking=MyMaskingRule("#########", ('pass', 'card') ) )


Django App Usage
================

**settings.py**

.. code::

    APP_ERROR_MASKING_MODULE="path to MyMaskingRule"
    APP_ERROR_MASKED_KEY_HAS = ('pass', 'card')
    APP_ERROR_MASKED_WITH = "############"