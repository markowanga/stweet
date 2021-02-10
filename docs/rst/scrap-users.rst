Download users
==============

Stweet allow to scrap user by usernames.

Scrapping users is simmilar to scrap tweets by ids.

.. code:: python

    import stweet as st

Prepare task
------------

Task named ``GetUsersTask`` which contains only one property –
``usernames: List[str]``. It contains list of usernames of users to
scrap.

.. code:: python

    usernames = ['ProtasiewiczJ', 'donaldtuskEPP']
    task = st.GetUsersTask(usernames)

Prepare UserOutputs
-------------------

Here is example of use UserOutputs. All options are in user-output
section.

.. code:: python

    user_collector = st.CollectorUserOutput()
    outputs = [user_collector]

Example task execution
----------------------

``GetUsersRunner`` executes the ``GetUsersTask``. It always needs to
input a ``get_user_task`` and ``user_outputs``. Below are all class
properties: - **``get_user_task: GetUsersTask``** – task with defined
users to scrap - **``user_outputs: List[UserOutput]``** – output of
scrapped tweets -
**``get_user_context: Optional[GetUsersContext] = None``** – context of
scrapping user - **``web_client: WebClient = RequestsWebClient()``** –
web client to make http requests -
**``auth_token_provider_factory: AuthTokenProviderFactory = SimpleAuthTokenProviderFactory()``**
– provider of auth token

.. code:: python

    result = st.GetUsersRunner(task, outputs).run()
    result




.. parsed-literal::

    GetUsersResult(users_count=2)


