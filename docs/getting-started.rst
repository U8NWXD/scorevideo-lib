***************
Getting Started
***************

Our code is hosted here: https://github.com/U8NWXD/scorevideo_lib

=================================
Getting the Code and Dependencies
=================================

#. Choose where you want to download the code, and navigate to that directory.
   Then download the code.

    .. code-block:: console

      $ cd path/to/desired/directory
      $ git clone https://github.com/U8NWXD/scorevideo_lib

#. Install python 3 from https://python.org or via your favorite package manager

#. Install ``virtualenv``

    .. code-block:: console

      $ pip3 install virtualenv

#. If you get a note from ``pip`` about ``virtualenv`` not being in your
   ``PATH``, you need to perform this step. ``PATH`` is a variable accessible
   from any bash terminal you run, and it tells bash where to look for the
   commands you enter. It is a list of directories separated by ``:``. You can
   see yours by running ``echo $PATH``. To run ``virtualenv`` commands, you need
   to add python's packages to your ``PATH`` by editing or creating the file
   ``~/.bash_profile`` on MacOS. To that file add the following lines:

    .. code-block:: console

      PATH="<Path from pip message>:$PATH"
      export PATH

#. Then you can install dependencies into a virtual environment

    .. code-block:: console

      $ cd scorevideo_lib
      $ virtualenv -p python3 venv
      $ source venv/bin/activate
      $ pip install -r requirements.txt

Now you're ready to use the library! You can check out the API reference
`here <modules>`_.

.. note:: If your data is from dyad assays and structured accordingly, you can
    transfer lights-on marks my running
    the ``transfer_lights_on_marks.py`` tool in the directory of log files like
    so: ``python transfer_lights_on_marks.py``. If you aren't sure if these
    requirements are met, they probably aren't. This is only useful for a few
    researchers.