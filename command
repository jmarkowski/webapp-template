#!/usr/bin/env bash
script=$0

#
# Constants
#
GREY='\033[0;37m'
NONE='\033[0m'

APP_IS_NOT_RUNNING=$(cat <<_EOF
The 'application' service is required and is not running.
You can start it with 'docker-compose up -d application'
or simply 'docker-compose up' to run all the services.
_EOF
)

function exec_cmd() {
  echo -e command: ${GREY}${@}${NONE}'\n'
  $@
}

function cmd_app() {
  APP_PID=$(docker-compose ps -q application)
  if [[ -z $APP_PID ]]; then
    echo "$APP_IS_NOT_RUNNING";
    return
  fi

  case "$1" in
    "bash")
      exec_cmd docker-compose exec application bash
      ;;

    "flask")
      case "$2" in
        "shell")
          exec_cmd docker-compose exec application flask shell
          ;;

        *)
          echo "$script app flask shell"
          ;;
      esac
      ;;

    "lint")
      exec_cmd docker-compose exec application ./command lint
      ;;

    "test")
      exec_cmd docker-compose exec application ./command test
      ;;

    *)
      echo "$script app [bash|flask|lint|test]"
      ;;
  esac
}

function cmd_db() {
  case "$1" in
    "bash")
      exec_cmd docker-compose exec -u postgres sql_database bash
      ;;

    "connect")
      docker-compose exec -u postgres sql_database psql
      ;;

    *)
      echo "$script db [bash|connect]"
      ;;
  esac
}

case "$1" in
  "app")
    cmd_app ${@:2}
    ;;

  "db")
    cmd_db ${@:2}
    ;;

  *)
    echo "$script [app|db]"
    ;;
esac
