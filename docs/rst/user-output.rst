UserOutput
==========

``UserOutput`` is as generic class which can export scrapped users.

Under the hood it has abstract method
``export_users(users: List[User])``.

There are few implementations of ``UserOutput``

.. code:: ipython3

    import stweet as st

PrintUserOutput
---------------

``PrintUserOutput`` prints all scrapper user.

.. code:: ipython3

    st.PrintUserOutput();




.. parsed-literal::

    <stweet.user_output.print_user_output.PrintUserOutput at 0x7feda63becd0>



CollectorUserOutput
-------------------

``CollectorUserOutput`` collect users in memory. This is the best option
when sbd need to process small part of tweets.

To get all tweets you need to run ``get_scrapped_users()``.

.. code:: ipython3

    st.CollectorUserOutput();




.. parsed-literal::

    <stweet.user_output.collector_user_output.CollectorUserOutput at 0x7feda63be7f0>



CsvUserOutput
-------------

``CsvUserOutput`` stores users in csv file. It has two parameters
``file_location`` and ``add_header_on_start``.

When ``add_header_on_start`` is ``True`` header is adding only when file
is empty. It is possible to continue storing the users in file in next
tasks.

.. code:: ipython3

    st.CsvUserOutput(
        file_location='my_csv_file.csv',
        add_header_on_start=True
    );




.. parsed-literal::

    <stweet.user_output.csv_user_output.CsvUserOutput at 0x7feda7964f10>



JsonLineFileUserOutput
----------------------

``JsonLineFileUserOutput`` stores users in file in json lines. This
solution is better because it can be problem with fast saving new user
in large files, also it can be problem with reading. Using json lines it
is possible to read line by line, without read whole document into
memory.

Class have only one property – ``file_name``, this is the file to store
users in json line format.

.. code:: ipython3

    st.JsonLineFileUserOutput(
        file_name='my_jl_file.jl'
    );




.. parsed-literal::

    <stweet.user_output.json_line_file_user_output.JsonLineFileUserOutput at 0x7feda63beb80>



PrintEveryNUserOutput
---------------------

``PrintEveryNUserOutput`` print event N-th scrapped user. This is best
solution to track that new users are scrapping.

Class have only one parameter – ``each_n``, this is the N value
described above.

.. code:: ipython3

    st.PrintEveryNUserOutput(
        each_n=100
    );




.. parsed-literal::

    <stweet.user_output.print_every_n_user_output.PrintEveryNUserOutput at 0x7feda63be6a0>


