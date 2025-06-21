#!/bin/bash

# Function to display help message
show_help() {
  echo "Usage: ./run.sh [options]"
  echo ""
  echo "Options:"
  echo "  --backend      Start the backend server"
  echo "  --web          Start the web application"
  echo "  --electron     Start the Electron desktop client"
  echo "  --all          Start all components"
  echo "  --help         Display this help message"
  echo ""
  echo "Examples:"
  echo "  ./run.sh --backend"
  echo "  ./run.sh --web"
  echo "  ./run.sh --electron"
  echo "  ./run.sh --all"
}

# Function to start the backend server
start_backend() {
  echo "Starting backend server..."
  cd backend
  pip install -r requirements.txt
  uvicorn app.main:app --reload --host 0.0.0.0 --port 12000
}

# Function to start the web application
start_web() {
  echo "Starting web application..."
  cd client/web
  npm install
  npm run dev
}

# Function to start the Electron desktop client
start_electron() {
  echo "Starting Electron desktop client..."
  cd client/electron
  npm install
  npm start
}

# Check if no arguments were provided
if [ $# -eq 0 ]; then
  show_help
  exit 1
fi

# Parse command line arguments
for arg in "$@"
do
  case $arg in
    --backend)
      start_backend
      shift
      ;;
    --web)
      start_web
      shift
      ;;
    --electron)
      start_electron
      shift
      ;;
    --all)
      # Start all components in separate terminals
      gnome-terminal --tab --title="Backend" -- bash -c "cd $(pwd) && ./run.sh --backend; exec bash"
      gnome-terminal --tab --title="Web" -- bash -c "cd $(pwd) && ./run.sh --web; exec bash"
      gnome-terminal --tab --title="Electron" -- bash -c "cd $(pwd) && ./run.sh --electron; exec bash"
      shift
      ;;
    --help)
      show_help
      exit 0
      ;;
    *)
      echo "Unknown option: $arg"
      show_help
      exit 1
      ;;
  esac
done