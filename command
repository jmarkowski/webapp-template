#!/usr/bin/env bash
script=$0

#
# Constants
#
GREY='\033[0;37m'
NONE='\033[0m'
CURDIR=$(dirname $(realpath $script))
APP_PATH=$CURDIR/application

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
          echo -e "\nUsage:";
          echo "  $script app flask [COMMAND]";
          echo -e "\nCommands:";
          echo "  shell     Start an interactive flask shell";
          ;;
      esac
      ;;

    "lint")
      exec_cmd docker-compose exec application ./command lint
      ;;

    "test")
      exec_cmd docker-compose exec application ./command test ${@:2}
      ;;

    *)
      echo -e "\nUsage:";
      echo "  $script app [COMMAND]";
      echo -e "\nCommands:";
      echo "  bash      Start a bash session";
      echo "  flask     Execute subcommands for a running flask instance";
      echo "  lint      Run the static code analysis (linter) against the code";
      echo "  test [m]  Run all the unit tests or just module 'm'";
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
      echo -e "\nUsage:";
      echo "  $script db [COMMAND]";
      echo -e "\nCommands:";
      echo "  bash      Start a bash session within the database server";
      echo "  connect   Start an interactive database terminal (psql)";
      ;;
  esac
}

function cmd_start() {
  case "$1" in
    "maint")
      source .env
      docker-compose up -d sql_database
      docker-compose up -d sql_administration
      docker container run --rm -ti \
        --env-file .env \
        --network $NETWORK_NAME \
        --volume $APP_PATH:/home/webapp \
        ${COMPOSE_PROJECT_NAME}/${APPLICATION_IMAGE} bash
      ;;

    *)
      echo -e "\nUsage:";
      echo "  $script start [COMMAND]";
      echo -e "\nCommands:";
      echo "  maint     Launch all the services, except the application";
      ;;
  esac
}

function cmd_stop() {
  case "$1" in
    "")
      exec_cmd docker-compose down
      ;;

    *)
      echo -e "\nUsage:";
      echo "  $script launch [COMMAND]";
      echo -e "\nCommands:";
      echo "  (default) Stop all services";
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

  "nginx")
    source .env
    docker container exec -ti \
      --workdir=/etc/nginx \
      --user nginx:nginx \
      ${COMPOSE_PROJECT_NAME}_reverse_proxy bash
    ;;

  "npm")
    source .env
    docker container run --rm -ti \
      --volume=$APP_PATH:/application \
      --workdir=/application \
      --user $(id -u):$(id -g) \
      ${COMPOSE_PROJECT_NAME}/${NODE_TOOLS_IMAGE} bash
    ;;

  "start")
    cmd_start ${@:2}
    ;;

  "stop")
    cmd_stop ${@:2}
    ;;

  *)
    echo -e "\nUsage:";
    echo "  $script [COMMAND]";
    echo -e "\nCommands:";
    echo "  app       Execute subcommands for a running application server";
    echo "  db        Execute subcommands for a running database server";
    echo "  nginx     Start a bash shell in the reverse-proxy";
    echo "  npm       Start an npm environment for managing node modules";
    echo "  start     Execute subcommands for starting the service";
    echo "  stop      Execute subcommands for stopping the service";
    ;;
esac
