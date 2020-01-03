# starlette-test

starlette and uvicorn fiddling, logging setup with logman script

## Requirements

Python 3.6+ and packages in `requirements.txt`

```bash
pip install -r requirements.txt
```

## Usage

Either `python example.py`

```bash
[2020-01-03T11:04:00.381] [INFO] Starting Starlette server! (example - example.py:77)
[2020-01-03T11:04:00.388] [INFO] Running uvicorn from example.py (uvicorn - example.py:79)
[2020-01-03T11:04:00.450] [INFO] Started server process [21320] (uvicorn.error - main.py:389)
[2020-01-03T11:04:00.460] [INFO] Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit) (uvicorn.error - main.py:471)
[2020-01-03T11:04:00.462] [INFO] Waiting for application startup. (uvicorn.error - on.py:22)
[2020-01-03T11:04:00.463] [INFO] Application startup complete. (uvicorn.error - on.py:34)
[2020-01-03T11:04:03.178] [INFO] hello world this is homepage (example - example.py:54)
[2020-01-03T11:04:03.183] [INFO] 127.0.0.1:51166 - "GET / HTTP/1.1" 200 (uvicorn.error - h11_impl.py:454)
```

or `uvicorn example:app`

```bash
[2020-01-03T11:05:40.768] [INFO] Started server process [24836] (uvicorn.error - main.py:389)
[2020-01-03T11:05:40.775] [INFO] Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit) (uvicorn.error - main.py:471)
[2020-01-03T11:05:40.777] [INFO] Waiting for application startup. (uvicorn.error - on.py:22)
[2020-01-03T11:05:40.777] [INFO] Application startup complete. (uvicorn.error - on.py:34)
[2020-01-03T11:05:45.133] [INFO] hello world this is homepage (example - example.py:54)
[2020-01-03T11:05:45.142] [INFO] 127.0.0.1:51241 - "GET / HTTP/1.1" 200 (uvicorn.error - h11_impl.py:454)
```

Note: regarding logger `uvicorn.error`, these appear when configuring `uvicorn.access`, propably something fishy in the current uvicorn (version `0.11.1`) internal logging setup .. might want to file an issue on that on [encode/uvicorn](https://github.com/encode/uvicorn/issues) after taking a closer look at it .. migth also want to mention the need for

```python
uvicorn.config.LOGGING_CONFIG['loggers'] = {}
logging.getLogger('').handlers = []
```

to get rid of a streamhandler otherwise created by uvicorn.
