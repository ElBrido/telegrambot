const express = require('express');
const session = require('express-session');
const bodyParser = require('body-parser');
const path = require('path');
require('dotenv').config();
const helmet = require('helmet');
const cors = require('cors');
const rateLimit = require('express-rate-limit');

// Import routes
const authRoutes = require('./routes/auth');
const dashboardRoutes = require('./routes/dashboard');
const planRoutes = require('./routes/plans');
const orderRoutes = require('./routes/orders');
const serverRoutes = require('./routes/servers');
const paymentRoutes = require('./routes/payment');

// Import database
const db = require('./config/database');

const app = express();
const PORT = process.env.PORT || 3000;

// Security middleware
app.use(helmet({
    contentSecurityPolicy: {
        directives: {
            defaultSrc: ["'self'"],
            styleSrc: ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com", "https://cdnjs.cloudflare.com"],
            fontSrc: ["'self'", "https://fonts.gstatic.com", "https://cdnjs.cloudflare.com"],
            scriptSrc: ["'self'", "'unsafe-inline'", "https://js.stripe.com", "https://cdnjs.cloudflare.com"],
            frameSrc: ["https://js.stripe.com"],
            connectSrc: ["'self'", "https://api.stripe.com"]
        }
    }
}));

// CORS configuration
app.use(cors({
    origin: process.env.APP_URL || 'http://localhost:3000',
    credentials: true
}));

// Rate limiting
const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // limit each IP to 100 requests per windowMs
    message: 'Too many requests from this IP, please try again later.'
});
app.use('/api/', limiter);

// Body parser middleware
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Session middleware
app.use(session({
    secret: process.env.SESSION_SECRET || 'your-secret-key-change-this',
    resave: false,
    saveUninitialized: false,
    cookie: {
        secure: process.env.NODE_ENV === 'production',
        httpOnly: true,
        maxAge: 24 * 60 * 60 * 1000 // 24 hours
    }
}));

// Static files
app.use(express.static(path.join(__dirname, 'public')));

// View engine setup
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Make user available to all views
app.use((req, res, next) => {
    res.locals.user = req.session.user || null;
    res.locals.isAuthenticated = !!req.session.user;
    
    // Override render to use layout
    const originalRender = res.render;
    res.render = function(view, locals = {}, callback) {
        // Don't wrap if it's already a layout or partial
        if (view === 'layout' || view.startsWith('partials/')) {
            return originalRender.call(this, view, locals, callback);
        }
        
        // Render the view to get its content
        originalRender.call(this, view, locals, (err, html) => {
            if (err) return callback ? callback(err) : next(err);
            
            // Merge locals with layout data
            const layoutLocals = {
                ...res.locals,
                ...locals,
                body: html,
                process: process // Make process.env available in layout
            };
            
            // Render with layout
            originalRender.call(this, 'layout', layoutLocals, callback);
        });
    };
    
    next();
});

// Routes
app.use('/auth', authRoutes);
app.use('/dashboard', dashboardRoutes);
app.use('/plans', planRoutes);
app.use('/orders', orderRoutes);
app.use('/servers', serverRoutes);
app.use('/payment', paymentRoutes);

// Home route
app.get('/', (req, res) => {
    res.render('index');
});

// About route
app.get('/about', (req, res) => {
    res.render('about');
});

// Contact route
app.get('/contact', (req, res) => {
    res.render('contact');
});

// 404 handler
app.use((req, res) => {
    res.status(404).render('404');
});

// Error handler
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).render('error', { 
        error: process.env.NODE_ENV === 'development' ? err : {} 
    });
});

// Initialize database and start server
db.initialize().then(() => {
    app.listen(PORT, () => {
        console.log(`🚀 MBE Hosting Server running on port ${PORT}`);
        console.log(`🌐 Visit: http://localhost:${PORT}`);
    });
}).catch(err => {
    console.error('Failed to initialize database:', err);
    process.exit(1);
});

module.exports = app;
