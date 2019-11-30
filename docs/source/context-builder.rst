Custom Context Builder
----------------------
Having more and more context about failure always help in debugging, by default this app captures HTTP headers, URL parameters, any post data.
More data can be included  like data-center name, server details and any other, by default these details are not captured. Nonetheless these details can be captured using ContextBuilderMixin.
Error Tracker comes with two type of context builders DefaultFlaskContextBuilder and DefaultDjangoContextBuilder for Flask and Django respectively.
We can either reuse the same context builder or customize them as per our need.

**Using ContextBuilderMixin**

.. note::

    Implement get_context method of ContextBuilderMixin, default context builders capture *request body*, *headers* and URL parameters.

.. code::

  from error_tracker import ContextBuilderMixin
  class ContextBuilder(ContextBuilderMixin):
       def get_context(self, request, masking=None):
            # return context dictionary

Flask App Usage
===============

This custom context builder can be supplied as parameter of AppErrorTracker constructor.

.. code::

        error_tracker = AppErrorTracker(app=app, db=db,
                                        context_builder=ContextBuilder())

Django App Usage
================

Add path of the custom builder class to the settings file, this class should not take any arguments for constructions.

**settings.py**

.. code::

    APP_ERROR_CONTEXT_BUILDER_MODULE = "path to ContextBuilder class"

