const { app, BrowserWindow, ipcMain, Tray, Menu, dialog, shell, systemPreferences } = require('electron');
const path = require('path');
const url = require('url');
const axios = require('axios');
const Store = require('electron-store');
const screenshot = require('screenshot-desktop');
const os = require('os');
const moment = require('moment');

// Initialize store for settings
const store = new Store();

// Global variables
let mainWindow;
let tray;
let isTracking = false;
let currentShift = null;
let screenshotInterval;
let activityCheckInterval;
let lastActivity = Date.now();
let apiBaseUrl = store.get('apiBaseUrl') || 'http://localhost:12000/api/v1';

// Create the main window
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1000,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      enableRemoteModule: true
    },
    icon: path.join(__dirname, 'assets/icons/icon.png')
  });

  // Load the index.html file
  mainWindow.loadURL(url.format({
    pathname: path.join(__dirname, 'index.html'),
    protocol: 'file:',
    slashes: true
  }));

  // Open DevTools in development
  if (process.env.NODE_ENV === 'development') {
    mainWindow.webContents.openDevTools();
  }

  // Handle window close
  mainWindow.on('close', (event) => {
    if (isTracking) {
      const choice = dialog.showMessageBoxSync(mainWindow, {
        type: 'question',
        buttons: ['Minimize to Tray', 'Stop Tracking and Quit', 'Cancel'],
        title: 'Confirm',
        message: 'You are currently tracking time. What would you like to do?'
      });

      switch (choice) {
        case 0: // Minimize to tray
          event.preventDefault();
          mainWindow.hide();
          break;
        case 1: // Stop tracking and quit
          stopTracking();
          break;
        case 2: // Cancel
          event.preventDefault();
          break;
      }
    }
  });

  // Handle window closed
  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  // Create tray icon
  createTray();

  // Check for screen recording permissions on macOS
  checkPermissions();
}

// Create tray icon
function createTray() {
  tray = new Tray(path.join(__dirname, 'assets/icons/tray-icon.png'));
  
  const contextMenu = Menu.buildFromTemplate([
    { 
      label: 'Open Insightful', 
      click: () => { 
        mainWindow.show(); 
      } 
    },
    { 
      label: 'Start Tracking', 
      click: () => { 
        if (!isTracking) {
          mainWindow.webContents.send('start-tracking-from-tray');
        }
      },
      enabled: !isTracking
    },
    { 
      label: 'Stop Tracking', 
      click: () => { 
        if (isTracking) {
          stopTracking();
        }
      },
      enabled: isTracking
    },
    { type: 'separator' },
    { 
      label: 'Quit', 
      click: () => { 
        if (isTracking) {
          const choice = dialog.showMessageBoxSync({
            type: 'question',
            buttons: ['Cancel', 'Stop Tracking and Quit'],
            title: 'Confirm',
            message: 'You are currently tracking time. Stop tracking and quit?'
          });

          if (choice === 1) {
            stopTracking();
            app.quit();
          }
        } else {
          app.quit();
        }
      } 
    }
  ]);
  
  tray.setToolTip('Insightful Time Tracker');
  tray.setContextMenu(contextMenu);
  
  tray.on('click', () => {
    mainWindow.isVisible() ? mainWindow.hide() : mainWindow.show();
  });
}

// Check for required permissions
function checkPermissions() {
  if (process.platform === 'darwin') {
    const screenCaptureStatus = systemPreferences.getMediaAccessStatus('screen');
    
    if (screenCaptureStatus !== 'granted') {
      dialog.showMessageBox(mainWindow, {
        type: 'warning',
        title: 'Permissions Required',
        message: 'Screen recording permission is required for this app to function properly.',
        buttons: ['Open System Preferences', 'Later'],
        defaultId: 0
      }).then(result => {
        if (result.response === 0) {
          systemPreferences.askForMediaAccess('screen');
        }
      });
    }
  }
}

// Start time tracking
async function startTracking(data) {
  try {
    const token = store.get('token');
    if (!token) {
      throw new Error('Not logged in');
    }

    const response = await axios.post(`${apiBaseUrl}/time-tracking/shift`, data, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    currentShift = response.data;
    isTracking = true;

    // Update tray context menu
    createTray();

    // Start taking screenshots
    startScreenshotCapture();

    // Start activity monitoring
    startActivityMonitoring();

    return currentShift;
  } catch (error) {
    console.error('Error starting tracking:', error);
    throw error;
  }
}

// Stop time tracking
async function stopTracking() {
  try {
    if (!currentShift) return;

    const token = store.get('token');
    if (!token) {
      throw new Error('Not logged in');
    }

    // Stop screenshot interval
    if (screenshotInterval) {
      clearInterval(screenshotInterval);
      screenshotInterval = null;
    }

    // Stop activity monitoring
    if (activityCheckInterval) {
      clearInterval(activityCheckInterval);
      activityCheckInterval = null;
    }

    const response = await axios.put(
      `${apiBaseUrl}/time-tracking/shift/${currentShift.id}`,
      { end: Date.now() },
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );

    isTracking = false;
    currentShift = null;

    // Update tray context menu
    createTray();

    // Notify renderer
    if (mainWindow) {
      mainWindow.webContents.send('tracking-stopped', response.data);
    }

    return response.data;
  } catch (error) {
    console.error('Error stopping tracking:', error);
    throw error;
  }
}

// Start screenshot capture
function startScreenshotCapture() {
  // Take screenshots every 5 minutes
  const screenshotFrequency = 5 * 60 * 1000; // 5 minutes in milliseconds
  
  // Take initial screenshot
  takeScreenshot();
  
  // Set interval for subsequent screenshots
  screenshotInterval = setInterval(takeScreenshot, screenshotFrequency);
}

// Take and upload screenshot
async function takeScreenshot() {
  try {
    if (!currentShift) return;

    const token = store.get('token');
    if (!token) return;

    // Get active window info
    const activeWindow = {
      app: 'Unknown',
      title: 'Unknown',
      url: ''
    };

    // Take screenshot
    const screenshotImg = await screenshot();
    
    // Convert to base64
    const screenshotBase64 = screenshotImg.toString('base64');

    // Get system permissions status
    const systemPermissions = {
      accessibility: 'authorized',
      screenAndSystemAudioRecording: process.platform === 'darwin' 
        ? systemPreferences.getMediaAccessStatus('screen') 
        : 'authorized'
    };

    // Prepare screenshot data
    const screenshotData = {
      employeeId: store.get('employeeId'),
      shiftId: currentShift.id,
      timestamp: Date.now(),
      organizationId: store.get('organizationId'),
      projectId: currentShift.projectId,
      taskId: currentShift.taskId,
      app: activeWindow.app,
      title: activeWindow.title,
      url: activeWindow.url,
      active: Date.now() - lastActivity < 5 * 60 * 1000, // Active if activity in last 5 minutes
      systemPermissions,
      screenshot: screenshotBase64
    };

    // Upload screenshot
    await axios.post(`${apiBaseUrl}/analytics/screenshot`, screenshotData, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    // Notify renderer
    if (mainWindow) {
      mainWindow.webContents.send('screenshot-taken');
    }
  } catch (error) {
    console.error('Error taking screenshot:', error);
  }
}

// Start activity monitoring
function startActivityMonitoring() {
  // Update last activity time
  lastActivity = Date.now();
  
  // Check activity every minute
  activityCheckInterval = setInterval(() => {
    // In a real implementation, we would track keyboard/mouse activity
    // For now, we'll just update the last activity time
    lastActivity = Date.now();
  }, 60 * 1000);
}

// App ready event
app.on('ready', createWindow);

// Quit when all windows are closed
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// Activate event
app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
  }
});

// IPC handlers
ipcMain.handle('login', async (event, credentials) => {
  try {
    const response = await axios.post(`${apiBaseUrl}/auth/login`, credentials);
    
    // Store token and user info
    store.set('token', response.data.access_token);
    store.set('employeeId', response.data.id);
    store.set('organizationId', response.data.organizationId);
    
    return response.data;
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
});

ipcMain.handle('logout', async () => {
  // Stop tracking if active
  if (isTracking) {
    await stopTracking();
  }
  
  // Clear stored data
  store.delete('token');
  store.delete('employeeId');
  store.delete('organizationId');
  
  return true;
});

ipcMain.handle('get-projects', async () => {
  try {
    const token = store.get('token');
    if (!token) {
      throw new Error('Not logged in');
    }
    
    const response = await axios.get(`${apiBaseUrl}/project`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    return response.data;
  } catch (error) {
    console.error('Error fetching projects:', error);
    throw error;
  }
});

ipcMain.handle('get-tasks', async (event, projectId) => {
  try {
    const token = store.get('token');
    if (!token) {
      throw new Error('Not logged in');
    }
    
    const response = await axios.get(`${apiBaseUrl}/task?projectId=${projectId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    return response.data;
  } catch (error) {
    console.error('Error fetching tasks:', error);
    throw error;
  }
});

ipcMain.handle('start-tracking', async (event, data) => {
  return await startTracking(data);
});

ipcMain.handle('stop-tracking', async () => {
  return await stopTracking();
});

ipcMain.handle('get-tracking-status', () => {
  return {
    isTracking,
    currentShift
  };
});

ipcMain.handle('open-external-link', (event, url) => {
  shell.openExternal(url);
});

ipcMain.handle('set-api-url', (event, url) => {
  apiBaseUrl = url;
  store.set('apiBaseUrl', url);
  return true;
});

ipcMain.handle('get-api-url', () => {
  return apiBaseUrl;
});

// Export functions for testing
module.exports = {
  startTracking,
  stopTracking
};