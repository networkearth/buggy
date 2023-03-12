#!/bin/bash
cd webapp/flask
python -m pytest
cd ../../api/flask
python -m pytest
cd ../../xlsform
python -m pytest
cd ../