#!/bin/bash

ansible-playbook django_messages/testapp/ansible_setup_test.yml \
&& python -m pytest \
&& ansible-playbook django_messages/testapp/ansible_teardown_test.yml