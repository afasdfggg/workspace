import moment from 'moment';

/**
 * Format date to readable string
 * @param {number|string|Date} date - Date to format
 * @param {string} format - Format string (default: 'MMM D, YYYY')
 * @returns {string} Formatted date string
 */
export const formatDate = (date, format = 'MMM D, YYYY') => {
  if (!date) return '';
  return moment(date).format(format);
};

/**
 * Format time to readable string
 * @param {number|string|Date} time - Time to format
 * @param {string} format - Format string (default: 'h:mm A')
 * @returns {string} Formatted time string
 */
export const formatTime = (time, format = 'h:mm A') => {
  if (!time) return '';
  return moment(time).format(format);
};

/**
 * Format date and time to readable string
 * @param {number|string|Date} datetime - Date and time to format
 * @param {string} format - Format string (default: 'MMM D, YYYY h:mm A')
 * @returns {string} Formatted date and time string
 */
export const formatDateTime = (datetime, format = 'MMM D, YYYY h:mm A') => {
  if (!datetime) return '';
  return moment(datetime).format(format);
};

/**
 * Format duration in milliseconds to readable string
 * @param {number} duration - Duration in milliseconds
 * @returns {string} Formatted duration string (e.g. "2h 30m")
 */
export const formatDuration = (duration) => {
  if (!duration) return '0h 0m';
  
  const hours = Math.floor(duration / (60 * 60 * 1000));
  const minutes = Math.floor((duration % (60 * 60 * 1000)) / (60 * 1000));
  
  return `${hours}h ${minutes}m`;
};

/**
 * Format duration in milliseconds to HH:MM:SS format
 * @param {number} duration - Duration in milliseconds
 * @returns {string} Formatted duration string (e.g. "02:30:45")
 */
export const formatDurationHHMMSS = (duration) => {
  if (!duration) return '00:00:00';
  
  const hours = Math.floor(duration / (60 * 60 * 1000));
  const minutes = Math.floor((duration % (60 * 60 * 1000)) / (60 * 1000));
  const seconds = Math.floor((duration % (60 * 1000)) / 1000);
  
  return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
};

/**
 * Get start and end of day in milliseconds
 * @param {number|string|Date} date - Date to get start and end of day
 * @returns {Object} Object with start and end properties
 */
export const getDayRange = (date = new Date()) => {
  const start = moment(date).startOf('day').valueOf();
  const end = moment(date).endOf('day').valueOf();
  
  return { start, end };
};

/**
 * Get start and end of week in milliseconds
 * @param {number|string|Date} date - Date to get start and end of week
 * @returns {Object} Object with start and end properties
 */
export const getWeekRange = (date = new Date()) => {
  const start = moment(date).startOf('week').valueOf();
  const end = moment(date).endOf('week').valueOf();
  
  return { start, end };
};

/**
 * Get start and end of month in milliseconds
 * @param {number|string|Date} date - Date to get start and end of month
 * @returns {Object} Object with start and end properties
 */
export const getMonthRange = (date = new Date()) => {
  const start = moment(date).startOf('month').valueOf();
  const end = moment(date).endOf('month').valueOf();
  
  return { start, end };
};

/**
 * Get relative time from now
 * @param {number|string|Date} date - Date to get relative time
 * @returns {string} Relative time string (e.g. "2 hours ago")
 */
export const fromNow = (date) => {
  if (!date) return '';
  return moment(date).fromNow();
};