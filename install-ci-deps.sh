#!/bin/bash
# Install Python and Ansible dependencies used by CI and review.
set -e
python -m pip install -U pip wheel setuptools
python -m pip install -r requirements-test.txt

cache=${CI_DEPS_CACHE:-"$HOME/.cache/ci-deps"}/ansible-collections
mkdir -p "$cache" "$HOME/.ansible"
if [ ! -e "$HOME/.ansible/collections" ]; then
  ln -s "$cache" "$HOME/.ansible/collections"
fi
ansible-galaxy collection install --upgrade "community.general:>=3.6.0"
ansible-galaxy role install --force -r molecule/resources/requirements.yml \
  -p "${CI_DEPS_CACHE:-$HOME/.cache/ci-deps}/ansible-roles"
