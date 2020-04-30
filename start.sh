#!/usr/bin/env bash
pyinstaller src/main.py --onefile --distpath ./bin -n elevate
if [[ $1 == "--run" || $1 == "run" ]]; then
    echo -e "\n\e[2;3m<-- Running with: ($@) -->\e[0m"
    cd lab
    shift
    ../bin/elevate $@
fi

if [[ $1 == "--serve" || $1 == "serve" ]]; then
    cp -r ./bin/elevate ./server/elevate
    cd ./server
    echo -e "\n\e[2;3m<-- Running with: ($@) -->\e[0m"
    shift
    ./elevate $@
    cd ..
fi