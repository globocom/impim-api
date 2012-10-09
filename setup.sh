#!/bin/bash

echo "instaling virtualenv..."
pip install virtualenv
rm -rf .venvs/
echo ".venvs/ removed!"
mkdir -p .venvs/
echo ".venvs/ created!"
echo "creating virtualenv .venvs/thumbor ..."
virtualenv .venvs/thumbor --no-site-packages
source .venvs/thumbor/bin/activate
echo "installing thumbor in their virtualenv..."
pip install thumbor
echo "deactive virtualenv .venvs/thumbor"
deactivate
