-- @bkapa8 and @byseishiro and Benson McBridge
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS licenses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    license_key VARCHAR(50) UNIQUE NOT NULL,
    user_id UUID REFERENCES users(id),
    type VARCHAR(20) DEFAULT 'pro', -- 'pro' ou 'enterprise'
    hardware_id VARCHAR(255),
    expires_at TIMESTAMP,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    license_id UUID REFERENCES licenses(id),
    amount DECIMAL(10,2),
    currency VARCHAR(3) DEFAULT 'USD',
    status VARCHAR(20),
    payment_method VARCHAR(50),
    stripe_payment_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS downloads (
    id SERIAL PRIMARY KEY,
    ip_address VARCHAR(45),
    user_agent TEXT,
    version VARCHAR(10),
    downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX idx_licenses_key ON licenses(license_key);
CREATE INDEX idx_licenses_user ON licenses(user_id);
CREATE INDEX idx_payments_user ON payments(user_id);
CREATE INDEX idx_payments_stripe ON payments(stripe_payment_id);