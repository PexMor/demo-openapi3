#!/usr/bin/env python3

from connexion import NoContent
from connexion.exceptions import OAuthProblem
import coloredlogs
import connexion
import hashlib
import logging
import logging.config
import os
import pathlib
import yaml

log_config = {
    'version': 1,
    'formatters': {
        'verbose2': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'verbose': {
            'format': '%(asctime)s %(module)s[%(process)d] %(levelname)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            "formatter": "verbose",
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "filename": "tmp/all_messages.log"
        }
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG',
        'formatter': 'verbose'
    }
}
fake_auth = True
TOKEN_DB = {
    'abcd': {
        'uid': 100
    }
}

upload_base = os.getenv("HOME")+"/upload"
pathlib.Path(upload_base).mkdir(parents=True, exist_ok=True)
pathlib.Path("tmp").mkdir(parents=True, exist_ok=True)

print(yaml.dump(log_config))
logging.config.dictConfig(log_config)
logger = logging.getLogger()
coloredlogs.install(level='DEBUG', logger=logger)

def api_key(token, required_scopes):
    if fake_auth:
        return {"uid": 100}
    info = TOKEN_DB.get(token, None)

    if not info:
        raise OAuthProblem('Invalid token')

    return info

def make_hash_path(base, hash):
    tdn = f"{base}/"+hash[0:1]+"/"+hash[0:2]
    pathlib.Path(tdn).mkdir(parents=True, exist_ok=True)
    tfn = f"{tdn}/{hash}"
    return tfn

def get_hash(hash_type, fname):
    h = hashlib.new(hash_type)
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def save_FileStorage_obj(fileStorageObj,hash_type,fn):
    fileStorageObj.save(fn)
    dyn_hash = get_hash(hash_type, fn)
    return dyn_hash

def cmd_create_flat(user_ref, body, **kwargs):
    logger.debug(f"Executing create environment belonging to user_ref={user_ref}")
    logger.debug(yaml.dump(body))
    fn = f"{upload_base}/tmp.bin"
    if "data" in kwargs:
        data = kwargs["data"]
        dyn_hash = save_FileStorage_obj(data,body['hash_type'],fn)
        logger.debug(
            f"hash type : {body['hash_type']}\n recv: {hash}\n real: {dyn_hash}")
        tfn = make_hash_path(upload_base, dyn_hash)
        os.rename(fn, tfn)
        hash_path = f"~/upload/{dyn_hash[0:1]}/{dyn_hash[0:2]}/{dyn_hash}"
        if dyn_hash == body['hash']:
            info = {
                "rc": 0, 
                "result": "ok", 
                "details": f"{body['hash_type']}/{body['hash']}", 
                "path": hash_path
            }
        else:
            info = {
                "rc": -1,
                "result": "hash errror, saved anyway",
                "details": f"{body['hash_type']}: {body['hash']} != {dyn_hash}",
                "path": hash_path
            }
    else:
        info = {
            "rc": 0,
            "result": "no file provided",
            "body": body
        }
    return info

def cmd_create_json(*args,**kwargs):
    print(f"received args:",yaml.dump(args))
    print(f"received kwargs:",yaml.dump(kwargs))
    return {"error":"not-implemented properly"},400

print(f"\ninvoked with __name__ = '{__name__}'\n")

if __name__ == '__main__':
    webApp = connexion.App(__name__, options={"swagger_ui": True})
    # CORS(webApp.app)
    webApp.add_api('apiDesc.yaml')
    # set the WSGI application callable to allow using uWSGI:
    # uwsgi --http :8080 -w app
    # application = app.app
    port = 8080
    print(f"Open http://localhost:{port}/v1/ui/")
    webApp.run(port=port)
    
