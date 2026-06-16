#!/bin/bash

source .venv/bin/activate
uvicorn backend:app --reload
