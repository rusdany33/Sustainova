const jwt = require('jsonwebtoken');
const { secret } = require('../config/env').jwt;
const query = require('../utils/db');

const verifyToken = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];

  if (!token) {
    return res.status(401).json({ message: 'No token provided' });
  }

  jwt.verify(token, secret, async (err, decoded) => {
    if (err) {
      return res.status(401).json({ message: 'Invalid token', error: err.message });
    }
    try {
      const users = await query('SELECT session_version FROM users WHERE ID_user = ?', [decoded.ID_user]);
      if (!users.length || users[0].session_version !== (decoded.session_version || 0)) {
        return res.status(401).json({ message: 'Sesi sudah berakhir. Silakan login kembali.' });
      }
      req.user = decoded;
      next();
    } catch (error) { next(error); }
  });
};

const authorize = (...allowedRoles) => {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({ message: 'User not authenticated' });
    }

    if (!allowedRoles.includes(req.user.role)) {
      return res.status(403).json({ 
        message: 'Access denied', 
        requiredRoles: allowedRoles,
        userRole: req.user.role 
      });
    }
    next();
  };
};

module.exports = {
  verifyToken,
  authorize
};
