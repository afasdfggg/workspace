# Insightful Time Tracker Desktop Client

A desktop application for tracking time and capturing screenshots for remote workers.

## Features

- Time tracking for projects and tasks
- Automatic screenshot capture
- Activity monitoring
- Project and task management
- Offline support
- System tray integration

## Installation

### Prerequisites

- Node.js 14+
- npm or yarn

### Setup

1. Clone the repository
2. Install dependencies:

```bash
cd client/electron
npm install
```

3. Run the application:

```bash
npm start
```

## Building for Distribution

To build the application for distribution:

```bash
# For all platforms
npm run dist

# For specific platforms
npm run dist -- --mac
npm run dist -- --win
npm run dist -- --linux
```

## Configuration

The application can be configured through the Settings screen:

- API URL: The URL of the backend API
- Screenshot Interval: How often screenshots are taken
- Start on Login: Whether the application starts automatically on system login
- Minimize to Tray: Whether the application minimizes to the system tray when closed

## Usage

1. Log in with your employee credentials
2. Select a project and task to track time for
3. Click "Start Tracking" to begin tracking time
4. The application will automatically take screenshots at the configured interval
5. Click "Stop Tracking" to stop tracking time

## License

This project is licensed under the MIT License - see the LICENSE file for details.