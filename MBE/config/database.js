const { Pool } = require('pg');
const crypto = require('crypto');

// Database connection pool
const pool = new Pool({
    host: process.env.DB_HOST || 'localhost',
    port: process.env.DB_PORT || 5432,
    database: process.env.DB_NAME || 'mbe_hosting',
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    max: 20,
    idleTimeoutMillis: 30000,
    connectionTimeoutMillis: 2000,
});

// Encryption functions
const ALGORITHM = 'aes-256-gcm';
const ENCRYPTION_KEY = Buffer.from(process.env.ENCRYPTION_KEY || crypto.randomBytes(32).toString('hex').slice(0, 32), 'utf8');

function encrypt(text) {
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv(ALGORITHM, ENCRYPTION_KEY, iv);
    let encrypted = cipher.update(text, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    const authTag = cipher.getAuthTag();
    return iv.toString('hex') + ':' + authTag.toString('hex') + ':' + encrypted;
}

function decrypt(text) {
    const parts = text.split(':');
    const iv = Buffer.from(parts[0], 'hex');
    const authTag = Buffer.from(parts[1], 'hex');
    const encryptedText = parts[2];
    const decipher = crypto.createDecipheriv(ALGORITHM, ENCRYPTION_KEY, iv);
    decipher.setAuthTag(authTag);
    let decrypted = decipher.update(encryptedText, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    return decrypted;
}

// Database initialization
async function initialize() {
    try {
        // Test connection
        await pool.query('SELECT NOW()');
        console.log('✅ Database connected successfully');

        // Create tables
        await createTables();
        console.log('✅ Database tables initialized');
    } catch (err) {
        console.error('❌ Database initialization error:', err);
        throw err;
    }
}

async function createTables() {
    const client = await pool.connect();
    try {
        await client.query('BEGIN');

        // Users table
        await client.query(`
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                first_name TEXT,
                last_name TEXT,
                phone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT true,
                email_verified BOOLEAN DEFAULT false
            )
        `);

        // Plans table
        await client.query(`
            CREATE TABLE IF NOT EXISTS plans (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                cpu INTEGER NOT NULL,
                ram INTEGER NOT NULL,
                disk INTEGER NOT NULL,
                databases INTEGER DEFAULT 0,
                backups INTEGER DEFAULT 0,
                price_monthly DECIMAL(10, 2) NOT NULL,
                is_custom BOOLEAN DEFAULT false,
                is_active BOOLEAN DEFAULT true,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        `);

        // Orders table
        await client.query(`
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                plan_id INTEGER REFERENCES plans(id),
                node_location VARCHAR(50),
                cpu INTEGER,
                ram INTEGER,
                disk INTEGER,
                databases INTEGER,
                backups INTEGER,
                price DECIMAL(10, 2) NOT NULL,
                status VARCHAR(50) DEFAULT 'pending',
                stripe_payment_intent_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        `);

        // Servers table
        await client.query(`
            CREATE TABLE IF NOT EXISTS servers (
                id SERIAL PRIMARY KEY,
                order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                pterodactyl_server_id INTEGER,
                server_name VARCHAR(255),
                node_location VARCHAR(50),
                cpu INTEGER,
                ram INTEGER,
                disk INTEGER,
                status VARCHAR(50) DEFAULT 'creating',
                ip_address TEXT,
                port INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        `);

        // Payments table
        await client.query(`
            CREATE TABLE IF NOT EXISTS payments (
                id SERIAL PRIMARY KEY,
                order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                amount DECIMAL(10, 2) NOT NULL,
                currency VARCHAR(3) DEFAULT 'USD',
                stripe_payment_intent_id TEXT,
                stripe_charge_id TEXT,
                status VARCHAR(50) DEFAULT 'pending',
                card_last4 VARCHAR(4),
                card_brand VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        `);

        // Sessions table for persistent sessions
        await client.query(`
            CREATE TABLE IF NOT EXISTS sessions (
                sid VARCHAR PRIMARY KEY,
                sess JSON NOT NULL,
                expire TIMESTAMP NOT NULL
            )
        `);

        await client.query('CREATE INDEX IF NOT EXISTS IDX_sessions_expire ON sessions(expire)');

        await client.query('COMMIT');
    } catch (err) {
        await client.query('ROLLBACK');
        throw err;
    } finally {
        client.release();
    }
}

// Insert default plans
async function insertDefaultPlans() {
    const client = await pool.connect();
    try {
        const checkPlans = await client.query('SELECT COUNT(*) FROM plans');
        if (parseInt(checkPlans.rows[0].count) === 0) {
            await client.query(`
                INSERT INTO plans (name, description, cpu, ram, disk, databases, backups, price_monthly, is_custom)
                VALUES 
                    ('Starter', 'Perfect for small projects and testing', 1, 2048, 20, 1, 2, 5.99, false),
                    ('Basic', 'Ideal for small websites and applications', 2, 4096, 40, 2, 5, 12.99, false),
                    ('Professional', 'Great for growing businesses', 4, 8192, 80, 5, 10, 24.99, false),
                    ('Enterprise', 'Maximum performance for large applications', 8, 16384, 160, 10, 20, 49.99, false),
                    ('Custom', 'Build your own plan', 0, 0, 0, 0, 0, 0, true)
            `);
            console.log('✅ Default plans inserted');
        }
    } catch (err) {
        console.error('Error inserting default plans:', err);
    } finally {
        client.release();
    }
}

module.exports = {
    pool,
    query: (text, params) => pool.query(text, params),
    initialize,
    insertDefaultPlans,
    encrypt,
    decrypt
};
