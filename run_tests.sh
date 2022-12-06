#!/bin/bash
cd webapp/flask
python -m pytest
cd ../../api/flask
python -m pytest
cd ../../xlsform
python -m pytest
cd ../push_to_inat/scripts
python -m pytest