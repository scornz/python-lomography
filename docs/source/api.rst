API
===

.. _api:

This page provides a detailed description of every class and function provided
by the `lomography` module. It is seperated into two sections: the synchronous
API and the asynchronous API. The synchronous API is a thin wrapper around the
asynchronous API, which is based on the `aiohttp` library. The synchronous API
is provided for convenience and ease of use, while the asynchronous API is
provided for performance and scalability.

Synchronous API
---------------

.. autoclass:: lomography.Lomography
   :members:
   :special-members:

.. autoclass:: lomography.LomoPhoto
   :members:

.. autoclass:: lomography.LomoCamera
   :members:

.. autoclass:: lomography.LomoFilm
   :members:

.. autoclass:: lomography.LomoUser
   :members:

.. autoclass:: lomography.LomoLens
   :members:

.. autoclass:: lomography.LomoTag
   :members:

Asynchronous API
----------------

.. autoclass:: lomography.AsyncLomography
   :members:
   :special-members:

.. autoclass:: lomography.AsyncLomoPhoto
   :members:

.. autoclass:: lomography.AsyncLomoCamera
   :members:

.. autoclass:: lomography.AsyncLomoFilm
   :members:

.. autoclass:: lomography.AsyncLomoUser
   :members:

.. autoclass:: lomography.AsyncLomoLens
   :members:

.. autoclass:: lomography.AsyncLomoTag
   :members:

Generic API
-----------
.. autoclass:: lomography.LomoImage
   :members:

.. autoclass:: lomography.LomoPhotoImage
   :members:
