#!/bin/bash
exec 3>&1
ansible-playbook django_messages/testapp/ansible_setup_test.yml \
&& EXITCODE=$(python -m pytest | tee >(grep -Po '\d+\sfailed' | grep -Po '\d+') >&3) \
&& ansible-playbook django_messages/testapp/ansible_teardown_test.yml \
&& exit ${EXITCODE}