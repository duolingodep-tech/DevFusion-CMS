==> Cloning from https://github.com/duolingodep-tech/DevFusion-CMS
==> Checking out commit 12bfd32155215d33a957a619cd3fa41acefcfc39 in branch main
==> Using Python version 3.14.3 (default)
==> Docs on specifying a Python version: https://render.com/docs/python-version
==> Installing Python version 3.14.3...
==> Using Poetry version 2.1.3 (default)
==> Docs on specifying a Poetry version: https://render.com/docs/poetry-version
==> Running build command 'pip install -r requirements.txt'...
Collecting Flask==3.0.3 (from -r requirements.txt (line 1))
  Downloading flask-3.0.3-py3-none-any.whl.metadata (3.2 kB)
Collecting Flask-SQLAlchemy==3.1.1 (from -r requirements.txt (line 2))
  Downloading flask_sqlalchemy-3.1.1-py3-none-any.whl.metadata (3.4 kB)
Collecting Werkzeug==3.0.3 (from -r requirements.txt (line 3))
  Downloading werkzeug-3.0.3-py3-none-any.whl.metadata (3.7 kB)
Collecting gunicorn==23.0.0 (from -r requirements.txt (line 4))
  Downloading gunicorn-23.0.0-py3-none-any.whl.metadata (4.4 kB)
Collecting Jinja2>=3.1.2 (from Flask==3.0.3->-r requirements.txt (line 1))
  Downloading jinja2-3.1.6-py3-none-any.whl.metadata (2.9 kB)
Collecting itsdangerous>=2.1.2 (from Flask==3.0.3->-r requirements.txt (line 1))
  Downloading itsdangerous-2.2.0-py3-none-any.whl.metadata (1.9 kB)
Collecting click>=8.1.3 (from Flask==3.0.3->-r requirements.txt (line 1))
  Downloading click-8.4.2-py3-none-any.whl.metadata (2.6 kB)
Collecting blinker>=1.6.2 (from Flask==3.0.3->-r requirements.txt (line 1))
  Downloading blinker-1.9.0-py3-none-any.whl.metadata (1.6 kB)
Collecting sqlalchemy>=2.0.16 (from Flask-SQLAlchemy==3.1.1->-r requirements.txt (line 2))
  Downloading sqlalchemy-2.0.51-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (9.5 kB)
Collecting MarkupSafe>=2.1.1 (from Werkzeug==3.0.3->-r requirements.txt (line 3))
  Downloading markupsafe-3.0.3-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (2.7 kB)
Collecting packaging (from gunicorn==23.0.0->-r requirements.txt (line 4))
  Downloading packaging-26.2-py3-none-any.whl.metadata (3.5 kB)
Collecting greenlet>=1 (from sqlalchemy>=2.0.16->Flask-SQLAlchemy==3.1.1->-r requirements.txt (line 2))
  Downloading greenlet-3.5.3-cp314-cp314-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl.metadata (3.8 kB)
Collecting typing-extensions>=4.6.0 (from sqlalchemy>=2.0.16->Flask-SQLAlchemy==3.1.1->-r requirements.txt (line 2))
  Downloading typing_extensions-4.16.0-py3-none-any.whl.metadata (3.3 kB)
Downloading flask-3.0.3-py3-none-any.whl (101 kB)
Downloading flask_sqlalchemy-3.1.1-py3-none-any.whl (25 kB)
Downloading werkzeug-3.0.3-py3-none-any.whl (227 kB)
Downloading gunicorn-23.0.0-py3-none-any.whl (85 kB)
Downloading blinker-1.9.0-py3-none-any.whl (8.5 kB)
Downloading click-8.4.2-py3-none-any.whl (119 kB)
Downloading itsdangerous-2.2.0-py3-none-any.whl (16 kB)
Downloading jinja2-3.1.6-py3-none-any.whl (134 kB)
Downloading markupsafe-3.0.3-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (23 kB)
Downloading sqlalchemy-2.0.51-cp314-cp314-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (3.3 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.3/3.3 MB 62.3 MB/s  0:00:00
Downloading greenlet-3.5.3-cp314-cp314-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl (663 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 663.6/663.6 kB 23.7 MB/s  0:00:00
Downloading typing_extensions-4.16.0-py3-none-any.whl (45 kB)
Downloading packaging-26.2-py3-none-any.whl (100 kB)
Installing collected packages: typing-extensions, packaging, MarkupSafe, itsdangerous, greenlet, click, blinker, Werkzeug, sqlalchemy, Jinja2, gunicorn, Flask, Flask-SQLAlchemy
Successfully installed Flask-3.0.3 Flask-SQLAlchemy-3.1.1 Jinja2-3.1.6 MarkupSafe-3.0.3 Werkzeug-3.0.3 blinker-1.9.0 click-8.4.2 greenlet-3.5.3 gunicorn-23.0.0 itsdangerous-2.2.0 packaging-26.2 sqlalchemy-2.0.51 typing-extensions-4.16.0
[notice] A new release of pip is available: 25.3 -> 26.1.2
[notice] To update, run: pip install --upgrade pip
==> Uploading build...
==> Uploaded in 6.0s. Compression took 1.9s
==> Build successful 🎉
==> Deploying...
==> Setting WEB_CONCURRENCY=1 by default, based on available CPUs in the instance
==> Running 'gunicorn app:app'
[2026-07-03 15:16:39 +0000] [57] [INFO] Starting gunicorn 23.0.0
[2026-07-03 15:16:39 +0000] [57] [INFO] Listening at: http://0.0.0.0:10000 (57)
[2026-07-03 15:16:39 +0000] [57] [INFO] Using worker: sync
[2026-07-03 15:16:39 +0000] [59] [INFO] Booting worker with pid: 59
[2026-07-03 15:16:41,220] ERROR in app: Exception on / [HEAD]
Traceback (most recent call last):
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1969, in _exec_single_context
    self.dialect.do_execute(
    ~~~~~~~~~~~~~~~~~~~~~~~^
        cursor, str_statement, effective_parameters, context
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
sqlite3.OperationalError: no such table: setting
The above exception was the direct cause of the following exception:
Traceback (most recent call last):
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/flask/app.py", line 1473, in wsgi_app
    response = self.full_dispatch_request()
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/flask/app.py", line 882, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/flask/app.py", line 878, in full_dispatch_request
    rv = self.preprocess_request()
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/flask/app.py", line 1253, in preprocess_request
    rv = self.ensure_sync(before_func)()
  File "/opt/render/project/src/app.py", line 180, in guard
    setup()
    ~~~~~^^
  File "/opt/render/project/src/app.py", line 122, in setup
    if not setting(k):
           ~~~~~~~^^^
  File "/opt/render/project/src/app.py", line 95, in setting
    s = Setting.query.filter_by(key=key).first()
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/orm/query.py", line 2766, in first
    return self.limit(1)._iter().first()  # type: ignore
           ~~~~~~~~~~~~~~~~~~~^^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/orm/query.py", line 2864, in _iter
    result: Union[ScalarResult[_T], Result[_T]] = self.session.execute(
                                                  ~~~~~~~~~~~~~~~~~~~~^
        statement,
        ^^^^^^^^^^
        params,
        ^^^^^^^
        execution_options={"_sa_orm_load_options": self.load_options},
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/orm/session.py", line 2373, in execute
    return self._execute_internal(
           ~~~~~~~~~~~~~~~~~~~~~~^
        statement,
        ^^^^^^^^^^
    ...<4 lines>...
        _add_event=_add_event,
        ^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/orm/session.py", line 2271, in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
                          ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        self,
        ^^^^^
    ...<4 lines>...
        conn,
        ^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/orm/context.py", line 306, in orm_execute_statement
    result = conn.execute(
        statement, params or {}, execution_options=execution_options
    )
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1421, in execute
    return meth(
        self,
        distilled_parameters,
        execution_options or NO_OPTIONS,
    )
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/sql/elements.py", line 526, in _execute_on_connection
    return connection._execute_clauseelement(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        self, distilled_params, execution_options
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1643, in _execute_clauseelement
    ret = self._execute_context(
        dialect,
    ...<8 lines>...
        cache_hit=cache_hit,
    )
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1848, in _execute_context
    return self._exec_single_context(
           ~~~~~~~~~~~~~~~~~~~~~~~~~^
        dialect, context, statement, parameters
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1988, in _exec_single_context
    self._handle_dbapi_exception(
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        e, str_statement, effective_parameters, cursor, context
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 2365, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1969, in _exec_single_context
    self.dialect.do_execute(
    ~~~~~~~~~~~~~~~~~~~~~~~^
        cursor, str_statement, effective_parameters, context
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: setting
[SQL: SELECT setting.id AS setting_id, setting."key" AS setting_key, setting.value AS setting_value 
FROM setting 
WHERE setting."key" = ?
 LIMIT ? OFFSET ?]
[parameters: ('password', 1, 0)]
(Background on this error at: https://sqlalche.me/e/20/e3q8)
127.0.0.1 - - [03/Jul/2026:15:16:41 +0000] "HEAD / HTTP/1.1" 500 0 "-" "Go-http-client/1.1"
==> Your service is live 🎉
==> 
==> ///////////////////////////////////////////////////////////
==> 
==> Available at your primary URL https://devfusion-cms.onrender.com
==> 
==> ///////////////////////////////////////////////////////////
[2026-07-03 15:16:45,919] ERROR in app: Exception on / [GET]
Traceback (most recent call last):
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1969, in _exec_single_context
    self.dialect.do_execute(
    ~~~~~~~~~~~~~~~~~~~~~~~^
        cursor, str_statement, effective_parameters, context
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
sqlite3.OperationalError: no such table: setting
The above exception was the direct cause of the following exception:
Traceback (most recent call last):
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/flask/app.py", line 1473, in wsgi_app
    response = self.full_dispatch_request()
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/flask/app.py", line 882, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/flask/app.py", line 878, in full_dispatch_request
    rv = self.preprocess_request()
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/flask/app.py", line 1253, in preprocess_request
    rv = self.ensure_sync(before_func)()
  File "/opt/render/project/src/app.py", line 180, in guard
    setup()
    ~~~~~^^
  File "/opt/render/project/src/app.py", line 122, in setup
    if not setting(k):
           ~~~~~~~^^^
  File "/opt/render/project/src/app.py", line 95, in setting
    s = Setting.query.filter_by(key=key).first()
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/orm/query.py", line 2766, in first
    return self.limit(1)._iter().first()  # type: ignore
           ~~~~~~~~~~~~~~~~~~~^^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/orm/query.py", line 2864, in _iter
    result: Union[ScalarResult[_T], Result[_T]] = self.session.execute(
                                                  ~~~~~~~~~~~~~~~~~~~~^
        statement,
        ^^^^^^^^^^
        params,
        ^^^^^^^
        execution_options={"_sa_orm_load_options": self.load_options},
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/orm/session.py", line 2373, in execute
    return self._execute_internal(
           ~~~~~~~~~~~~~~~~~~~~~~^
        statement,
        ^^^^^^^^^^
    ...<4 lines>...
        _add_event=_add_event,
        ^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/orm/session.py", line 2271, in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
                          ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        self,
        ^^^^^
    ...<4 lines>...
        conn,
        ^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/orm/context.py", line 306, in orm_execute_statement
    result = conn.execute(
        statement, params or {}, execution_options=execution_options
    )
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1421, in execute
    return meth(
        self,
        distilled_parameters,
        execution_options or NO_OPTIONS,
    )
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/sql/elements.py", line 526, in _execute_on_connection
    return connection._execute_clauseelement(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        self, distilled_params, execution_options
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1643, in _execute_clauseelement
    ret = self._execute_context(
        dialect,
    ...<8 lines>...
        cache_hit=cache_hit,
    )
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1848, in _execute_context
    return self._exec_single_context(
           ~~~~~~~~~~~~~~~~~~~~~~~~~^
        dialect, context, statement, parameters
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1988, in _exec_single_context
    self._handle_dbapi_exception(
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        e, str_statement, effective_parameters, cursor, context
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 2365, in _handle_dbapi_exception
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/base.py", line 1969, in _exec_single_context
    self.dialect.do_execute(
    ~~~~~~~~~~~~~~~~~~~~~~~^
        cursor, str_statement, effective_parameters, context
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/render/project/src/.venv/lib/python3.14/site-packages/sqlalchemy/engine/default.py", line 952, in do_execute
    cursor.execute(statement, parameters)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: setting
[SQL: SELECT setting.id AS setting_id, setting."key" AS setting_key, setting.value AS setting_value 
FROM setting 
WHERE setting."key" = ?
 LIMIT ? OFFSET ?]
[parameters: ('password', 1, 0)]
(Background on this error at: https://sqlalche.me/e/20/e3q8)
127.0.0.1 - - [03/Jul/2026:15:16:45 +0000] "GET / HTTP/1.1" 500 265 "-" "Go-http-client/2.0"