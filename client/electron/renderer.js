// Import required modules
const { ipcRenderer } = require('electron');
const moment = require('moment');

// DOM Elements
// Login Screen
const loginScreen = document.getElementById('login-screen');
const mainScreen = document.getElementById('main-screen');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const loginBtn = document.getElementById('login-btn');
const loginError = document.getElementById('login-error');
const signupLink = document.getElementById('signup-link');

// Main Screen
const userNameElement = document.getElementById('user-name');
const logoutBtn = document.getElementById('logout-btn');
const navLinks = document.querySelectorAll('.nav-menu a');
const contentSections = document.querySelectorAll('.content-section');

// Dashboard
const todayTimeElement = document.getElementById('today-time');
const weekTimeElement = document.getElementById('week-time');
const activeProjectsElement = document.getElementById('active-projects');
const startTrackingBtn = document.getElementById('start-tracking-btn');
const stopTrackingBtn = document.getElementById('stop-tracking-btn');
const activityListElement = document.getElementById('activity-list');

// Projects
const projectsListElement = document.getElementById('projects-list');

// Time Tracking
const projectSelect = document.getElementById('project-select');
const taskSelect = document.getElementById('task-select');
const startTrackingFormBtn = document.getElementById('start-tracking-form-btn');
const currentTrackingElement = document.getElementById('current-tracking');
const trackingHistoryListElement = document.getElementById('tracking-history-list');

// Settings
const apiUrlInput = document.getElementById('api-url');
const screenshotIntervalSelect = document.getElementById('screenshot-interval');
const startOnLoginCheckbox = document.getElementById('start-on-login');
const minimizeToTrayCheckbox = document.getElementById('minimize-to-tray');
const saveSettingsBtn = document.getElementById('save-settings-btn');

// Footer
const trackingIndicator = document.getElementById('tracking-indicator');
const trackingStatusText = document.getElementById('tracking-status-text');
const trackingTimer = document.getElementById('tracking-timer');

// Global variables
let isTracking = false;
let currentShift = null;
let trackingStartTime = null;
let timerInterval = null;
let projects = [];
let tasks = [];
let user = null;

// Initialize the application
async function init() {
  // Check if user is logged in
  const token = localStorage.getItem('token');
  if (token) {
    try {
      // Get user info
      user = JSON.parse(localStorage.getItem('user'));
      
      // Show main screen
      showMainScreen();
      
      // Load data
      await loadData();
      
      // Check tracking status
      const status = await ipcRenderer.invoke('get-tracking-status');
      if (status.isTracking) {
        isTracking = true;
        currentShift = status.currentShift;
        startTrackingUI(currentShift);
      }
    } catch (error) {
      console.error('Error initializing app:', error);
      showLoginScreen();
    }
  } else {
    showLoginScreen();
  }
  
  // Load settings
  loadSettings();
}

// Show login screen
function showLoginScreen() {
  loginScreen.classList.remove('hidden');
  mainScreen.classList.add('hidden');
}

// Show main screen
function showMainScreen() {
  loginScreen.classList.add('hidden');
  mainScreen.classList.remove('hidden');
  
  // Set user name
  if (user) {
    userNameElement.textContent = user.name;
  }
}

// Load settings
async function loadSettings() {
  // Load API URL
  const apiUrl = await ipcRenderer.invoke('get-api-url');
  apiUrlInput.value = apiUrl;
  
  // Load other settings from localStorage
  screenshotIntervalSelect.value = localStorage.getItem('screenshotInterval') || '5';
  startOnLoginCheckbox.checked = localStorage.getItem('startOnLogin') === 'true';
  minimizeToTrayCheckbox.checked = localStorage.getItem('minimizeToTray') === 'true';
}

// Save settings
function saveSettings() {
  // Save API URL
  ipcRenderer.invoke('set-api-url', apiUrlInput.value);
  
  // Save other settings to localStorage
  localStorage.setItem('screenshotInterval', screenshotIntervalSelect.value);
  localStorage.setItem('startOnLogin', startOnLoginCheckbox.checked);
  localStorage.setItem('minimizeToTray', minimizeToTrayCheckbox.checked);
  
  // Show success message
  alert('Settings saved successfully!');
}

// Load data
async function loadData() {
  try {
    // Load projects
    projects = await ipcRenderer.invoke('get-projects');
    renderProjects();
    
    // Update project select
    updateProjectSelect();
    
    // Update dashboard stats
    updateDashboardStats();
    
    // Load tracking history
    loadTrackingHistory();
  } catch (error) {
    console.error('Error loading data:', error);
  }
}

// Update dashboard stats
function updateDashboardStats() {
  // Calculate today's time
  const todayTime = calculateTodayTime();
  todayTimeElement.textContent = formatDuration(todayTime);
  
  // Calculate week's time
  const weekTime = calculateWeekTime();
  weekTimeElement.textContent = formatDuration(weekTime);
  
  // Count active projects
  const activeProjectsCount = projects.filter(project => !project.archived).length;
  activeProjectsElement.textContent = activeProjectsCount;
}

// Calculate today's time
function calculateTodayTime() {
  // This would normally come from the API
  // For now, return a placeholder value
  return 3 * 60 * 60 * 1000; // 3 hours in milliseconds
}

// Calculate week's time
function calculateWeekTime() {
  // This would normally come from the API
  // For now, return a placeholder value
  return 15 * 60 * 60 * 1000; // 15 hours in milliseconds
}

// Format duration
function formatDuration(duration) {
  const hours = Math.floor(duration / (60 * 60 * 1000));
  const minutes = Math.floor((duration % (60 * 60 * 1000)) / (60 * 1000));
  return `${hours}h ${minutes}m`;
}

// Render projects
function renderProjects() {
  if (!projects || projects.length === 0) {
    projectsListElement.innerHTML = '<p class="empty-state">No projects found</p>';
    return;
  }
  
  let html = '';
  
  projects.forEach(project => {
    html += `
      <div class="project-card">
        <div class="project-header">
          <div class="project-name">${project.name}</div>
          <div class="project-badge ${project.archived ? 'badge-archived' : 'badge-active'}">
            ${project.archived ? 'Archived' : 'Active'}
          </div>
        </div>
        <div class="project-description">${project.description || 'No description'}</div>
        <div class="project-stats">
          <div class="project-stat">
            <div class="project-stat-label">Tasks</div>
            <div class="project-stat-value">${project.taskCount || 0}</div>
          </div>
          <div class="project-stat">
            <div class="project-stat-label">Team</div>
            <div class="project-stat-value">${project.employees ? project.employees.length : 0} members</div>
          </div>
        </div>
        <div class="project-actions">
          <button class="btn btn-primary track-project-btn" data-project-id="${project.id}">Track Time</button>
        </div>
      </div>
    `;
  });
  
  projectsListElement.innerHTML = html;
  
  // Add event listeners to track buttons
  document.querySelectorAll('.track-project-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const projectId = btn.getAttribute('data-project-id');
      showTimeTrackingSection(projectId);
    });
  });
}

// Update project select
function updateProjectSelect() {
  if (!projects || projects.length === 0) {
    projectSelect.innerHTML = '<option value="">No projects available</option>';
    return;
  }
  
  let html = '<option value="">Select a project</option>';
  
  projects.filter(project => !project.archived).forEach(project => {
    html += `<option value="${project.id}">${project.name}</option>`;
  });
  
  projectSelect.innerHTML = html;
}

// Load tasks for project
async function loadTasksForProject(projectId) {
  try {
    tasks = await ipcRenderer.invoke('get-tasks', projectId);
    updateTaskSelect();
  } catch (error) {
    console.error('Error loading tasks:', error);
    tasks = [];
    updateTaskSelect();
  }
}

// Update task select
function updateTaskSelect() {
  if (!tasks || tasks.length === 0) {
    taskSelect.innerHTML = '<option value="">No tasks available</option>';
    taskSelect.disabled = true;
    return;
  }
  
  let html = '<option value="">Select a task</option>';
  
  tasks.forEach(task => {
    html += `<option value="${task.id}">${task.name}</option>`;
  });
  
  taskSelect.innerHTML = html;
  taskSelect.disabled = false;
}

// Load tracking history
function loadTrackingHistory() {
  // This would normally come from the API
  // For now, use placeholder data
  const history = [
    {
      id: '1',
      projectId: 'p1',
      projectName: 'Website Redesign',
      taskId: 't1',
      taskName: 'Homepage Layout',
      start: Date.now() - 24 * 60 * 60 * 1000,
      end: Date.now() - 23 * 60 * 60 * 1000,
      duration: 60 * 60 * 1000 // 1 hour
    },
    {
      id: '2',
      projectId: 'p2',
      projectName: 'Mobile App Development',
      taskId: 't2',
      taskName: 'User Authentication',
      start: Date.now() - 48 * 60 * 60 * 1000,
      end: Date.now() - 46 * 60 * 60 * 1000,
      duration: 2 * 60 * 60 * 1000 // 2 hours
    }
  ];
  
  renderTrackingHistory(history);
  renderRecentActivity(history);
}

// Render tracking history
function renderTrackingHistory(history) {
  if (!history || history.length === 0) {
    trackingHistoryListElement.innerHTML = '<p class="empty-state">No tracking history found</p>';
    return;
  }
  
  let html = '';
  
  history.forEach(item => {
    html += `
      <div class="tracking-history-item">
        <div class="tracking-history-details">
          <div class="tracking-history-project">${item.projectName}</div>
          <div class="tracking-history-task">${item.taskName}</div>
          <div class="tracking-history-date">${moment(item.start).format('MMM D, YYYY')}</div>
        </div>
        <div class="tracking-history-duration">${formatDuration(item.duration)}</div>
      </div>
    `;
  });
  
  trackingHistoryListElement.innerHTML = html;
}

// Render recent activity
function renderRecentActivity(history) {
  if (!history || history.length === 0) {
    activityListElement.innerHTML = '<p class="empty-state">No recent activity</p>';
    return;
  }
  
  let html = '';
  
  history.forEach(item => {
    html += `
      <div class="activity-item">
        <div class="activity-time">${moment(item.end).fromNow()}</div>
        <div class="activity-description">Tracked time on ${item.taskName}</div>
        <div class="activity-project">${item.projectName}</div>
      </div>
    `;
  });
  
  activityListElement.innerHTML = html;
}

// Start tracking
async function startTracking(projectId, taskId) {
  try {
    if (isTracking) {
      await stopTracking();
    }
    
    const data = {
      type: 'manual',
      start: Date.now(),
      timezoneOffset: new Date().getTimezoneOffset() * 60 * 1000,
      employeeId: user.id,
      organizationId: user.organizationId,
      projectId: projectId,
      taskId: taskId
    };
    
    currentShift = await ipcRenderer.invoke('start-tracking', data);
    isTracking = true;
    
    startTrackingUI(currentShift);
    
    return currentShift;
  } catch (error) {
    console.error('Error starting tracking:', error);
    alert('Failed to start tracking. Please try again.');
  }
}

// Stop tracking
async function stopTracking() {
  try {
    if (!isTracking) return;
    
    const shift = await ipcRenderer.invoke('stop-tracking');
    isTracking = false;
    currentShift = null;
    
    stopTrackingUI();
    
    // Reload data to update history
    await loadData();
    
    return shift;
  } catch (error) {
    console.error('Error stopping tracking:', error);
    alert('Failed to stop tracking. Please try again.');
  }
}

// Start tracking UI
function startTrackingUI(shift) {
  // Update tracking indicator
  trackingIndicator.classList.add('tracking-active');
  trackingStatusText.textContent = 'Tracking';
  
  // Show stop button, hide start button
  startTrackingBtn.classList.add('hidden');
  stopTrackingBtn.classList.remove('hidden');
  
  // Update current tracking info
  updateCurrentTrackingInfo(shift);
  
  // Start timer
  trackingStartTime = shift.start;
  startTimer();
}

// Stop tracking UI
function stopTrackingUI() {
  // Update tracking indicator
  trackingIndicator.classList.remove('tracking-active');
  trackingStatusText.textContent = 'Not tracking';
  
  // Show start button, hide stop button
  startTrackingBtn.classList.remove('hidden');
  stopTrackingBtn.classList.add('hidden');
  
  // Clear current tracking info
  currentTrackingElement.innerHTML = '<p class="empty-state">Not tracking time</p>';
  
  // Stop timer
  stopTimer();
}

// Update current tracking info
function updateCurrentTrackingInfo(shift) {
  const project = projects.find(p => p.id === shift.projectId);
  const task = tasks.find(t => t.id === shift.taskId);
  
  let html = `
    <div class="tracking-project">${project ? project.name : 'Unknown Project'}</div>
  `;
  
  if (task) {
    html += `<div class="tracking-task">${task.name}</div>`;
  }
  
  html += `
    <div class="tracking-time">Started: ${moment(shift.start).format('h:mm A')}</div>
  `;
  
  currentTrackingElement.innerHTML = html;
}

// Start timer
function startTimer() {
  if (timerInterval) {
    clearInterval(timerInterval);
  }
  
  updateTimer();
  
  timerInterval = setInterval(updateTimer, 1000);
}

// Stop timer
function stopTimer() {
  if (timerInterval) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
  
  trackingTimer.textContent = '00:00:00';
}

// Update timer
function updateTimer() {
  if (!trackingStartTime) return;
  
  const elapsed = Date.now() - trackingStartTime;
  const duration = moment.duration(elapsed);
  
  const hours = String(Math.floor(duration.asHours())).padStart(2, '0');
  const minutes = String(duration.minutes()).padStart(2, '0');
  const seconds = String(duration.seconds()).padStart(2, '0');
  
  trackingTimer.textContent = `${hours}:${minutes}:${seconds}`;
}

// Show section
function showSection(sectionId) {
  // Hide all sections
  contentSections.forEach(section => {
    section.classList.add('hidden');
  });
  
  // Show selected section
  document.getElementById(`${sectionId}-section`).classList.remove('hidden');
  
  // Update active nav link
  navLinks.forEach(link => {
    link.parentElement.classList.remove('active');
    if (link.getAttribute('data-section') === sectionId) {
      link.parentElement.classList.add('active');
    }
  });
}

// Show time tracking section
function showTimeTrackingSection(projectId) {
  showSection('time-tracking');
  
  if (projectId) {
    projectSelect.value = projectId;
    loadTasksForProject(projectId);
  }
}

// Event Listeners
// Login form
loginBtn.addEventListener('click', async () => {
  const email = emailInput.value.trim();
  const password = passwordInput.value.trim();
  
  if (!email || !password) {
    loginError.textContent = 'Please enter both email and password';
    return;
  }
  
  try {
    const response = await ipcRenderer.invoke('login', { username: email, password });
    
    // Store user info
    user = response;
    localStorage.setItem('token', response.access_token);
    localStorage.setItem('user', JSON.stringify(response));
    
    // Show main screen
    showMainScreen();
    
    // Load data
    await loadData();
  } catch (error) {
    console.error('Login error:', error);
    loginError.textContent = 'Invalid email or password';
  }
});

// Signup link
signupLink.addEventListener('click', (e) => {
  e.preventDefault();
  ipcRenderer.invoke('open-external-link', 'https://app.insightful.io/signup');
});

// Logout button
logoutBtn.addEventListener('click', async () => {
  try {
    await ipcRenderer.invoke('logout');
    
    // Clear local storage
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    
    // Reset variables
    user = null;
    isTracking = false;
    currentShift = null;
    
    // Stop timer
    stopTimer();
    
    // Show login screen
    showLoginScreen();
  } catch (error) {
    console.error('Logout error:', error);
  }
});

// Navigation links
navLinks.forEach(link => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    const section = link.getAttribute('data-section');
    showSection(section);
  });
});

// Project select
projectSelect.addEventListener('change', () => {
  const projectId = projectSelect.value;
  if (projectId) {
    loadTasksForProject(projectId);
  } else {
    taskSelect.innerHTML = '<option value="">Select a project first</option>';
    taskSelect.disabled = true;
  }
});

// Start tracking button (dashboard)
startTrackingBtn.addEventListener('click', () => {
  showTimeTrackingSection();
});

// Stop tracking button
stopTrackingBtn.addEventListener('click', async () => {
  await stopTracking();
});

// Start tracking form button
startTrackingFormBtn.addEventListener('click', async () => {
  const projectId = projectSelect.value;
  const taskId = taskSelect.value;
  
  if (!projectId) {
    alert('Please select a project');
    return;
  }
  
  await startTracking(projectId, taskId || null);
});

// Save settings button
saveSettingsBtn.addEventListener('click', () => {
  saveSettings();
});

// IPC event listeners
ipcRenderer.on('start-tracking-from-tray', () => {
  showTimeTrackingSection();
});

ipcRenderer.on('tracking-stopped', async () => {
  isTracking = false;
  currentShift = null;
  stopTrackingUI();
  await loadData();
});

ipcRenderer.on('screenshot-taken', () => {
  // Update UI to show screenshot was taken
  const now = new Date();
  const timeString = now.toLocaleTimeString();
  
  // Add to activity list
  const newActivity = document.createElement('div');
  newActivity.className = 'activity-item';
  newActivity.innerHTML = `
    <div class="activity-time">just now</div>
    <div class="activity-description">Screenshot taken at ${timeString}</div>
    <div class="activity-project">${currentShift ? 'Current tracking session' : ''}</div>
  `;
  
  activityListElement.prepend(newActivity);
  
  // Remove empty state if present
  const emptyState = activityListElement.querySelector('.empty-state');
  if (emptyState) {
    emptyState.remove();
  }
});

// Initialize app
init();