#!/usr/bin/env bash
script=$0

#
# Constants
#
GREY='\033[0;37m'
NONE='\033[0m'

function exec_cmd() {
  echo -e command: ${GREY}${@}${NONE}'\n'
  $@
}

function cmd_app() {
  case "$1" in
    "test")
      exec_cmd docker-compose exec application ./command test
      ;;

    *)
      echo "$script app test"
      ;;
  esac
}

case "$1" in
  "app")
    cmd_app $2
    ;;

  *)
    echo "$script app"
    ;;
esac
