#!/usr/bin/env bash
uvicorn --host=0.0.0.0 app:app --workers=4
