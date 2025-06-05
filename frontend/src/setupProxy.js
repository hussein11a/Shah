const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  // Don't proxy /admin routes - let them be served as static files
  app.use('/admin', (req, res, next) => {
    // Serve static files from public/admin directory
    next();
  });
};