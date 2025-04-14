#!/bin/bash
shopt -s extglob
rm -vr !("uninstall.sh"|"generate.sh"|"main.py")
shopt -u extglob