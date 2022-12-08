#!/bin/bash
cd xlsform
pylint --rcfile standard.rc $(git ls-files '*.py')
cd ../webapp
pylint --rcfile standard.rc $(git ls-files '*.py')
cd ../api
pylint --rcfile standard.rc $(git ls-files '*.py')
cd ../push_to_inat
pylint --rcfile standard.rc $(git ls-files '*.py')
cd ../