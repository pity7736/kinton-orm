#!/usr/bin/env bash
pytest -s -vvv --cov=kinton --cov-report term-missing tests
