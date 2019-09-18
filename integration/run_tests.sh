#!/usr/bin/env bash

(cd integration/tests; PYTHONPATH=$(pwd) py.test)
