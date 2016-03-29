#!/bin/bash
find . -name "*.pyc" | xargs rm
find . -name "*.py~" | xargs rm
find . -name "*.html~" | xargs rm
