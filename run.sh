#!/bin/bash
cd app
gunicorn main:app
