Usage
=====

This page includes all the information you need to get started with
`python-lomography`. If you're looking for more detailed information, check
out the :ref:`API reference <api>`.

.. _installation:

Installation
------------

To use `python-lomography`, first install it using pip (or your package
manager of choice) by running the following command in your terminal:

.. code-block:: console

   pip install python-lomography

`python-lomography` is now installed! Let's go fetch some photos.

Getting Started
---------------

To get started, you'll need an API key from Lomography. You can get one by
requesting it from the Lomography team (more information can be found
`here <https://www.lomography.com/api/>`_).

Once you have your API key, you can start using `python-lomography` by
importing the `Lomography` class and creating an instance of it with your
API key:

.. code-block:: python

   from lomography import Lomography

   lomo = Lomography(api_key='your_api_key')
   # Your code here, fetching photos, cameras, film, etc.
   lomo.close()

You can now start fetching photos, cameras, film, etc. from the Lomography API.
In order to clean up the resources associated with the `Lomography` instance,
you should call the `close` method when you're done using it.

.. note::

   You can also execute all of this code in a `with` block, which will automatically
   clean up the associated resources for you:

   .. code-block:: python

      with Lomography(api_key='your_api_key') as lomo:
          # Your code here

Here are some examples of how you can use `python-lomography` to fetch photos,
cameras, film, etc. from the Lomography API.

Fetching Photos
~~~~~~~~~~~~~~~~
.. code-block:: python

   # Get most popular photos from the past month
   photos = lomo.fetch_popular_photos()
   for photo in photos:
      # Print the title of each photo
      print(photo.title)

   # Get the most recently uploaded photos
   photos = lomo.fetch_recent_photos()
   for photo in photos:
      # Print the title of each photo
      print(photo.title)

Camera Specific Photos
~~~~~~~~~~~~~~~~~~~~~~

We can also fetch photos taken with a specific camera. To do this, we first
need to get a list of cameras and then fetch photos taken with that camera.
We can also do this without fetching the list of cameras by using the camera's
unique ID (see :ref:`API reference <api>` for more information)

.. code-block:: python

   # Get five cameras
   cameras = lomo.fetch_cameras(amt=5)
   # Get photos taken with the first camera
   camera = cameras[0]

   # Get the most popular photos taken with the camera
   popular_photos = camera.fetch_popular_photos(amt=10)
   # Get the most popular photos taken with the camera
   recent_photos = camera.fetch_recent_photos(amt=10)

Film Specific Photos
~~~~~~~~~~~~~~~~~~~~~~

We can do the same with films.

.. code-block:: python

   # Get five films
   films = lomo.fetch_films(amt=5)
   # Get photos taken with the first film
   film = films[0]

   # Get the most popular photos taken with the film
   popular_photos = film.fetch_popular_photos(amt=10)
   # Get the most popular photos taken with the film
   recent_photos = film.fetch_recent_photos(amt=10)

For more information on the available methods, classes, and attributes, check
out the :ref:`API reference <api>`.
