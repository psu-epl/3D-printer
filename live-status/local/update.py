#!/usr/bin/env python
import api
import json

payload = json.dumps({"running": True})
api.update(payload)
