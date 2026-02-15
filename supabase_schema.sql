-- Supabase Schema for Anime Office Command Center
-- Run this in your Supabase SQL Editor to create the required tables

-- 1. Agent Status Table
CREATE TABLE IF NOT EXISTS agent_status (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_name TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('working', 'idle', 'completed', 'failed')),
    task_name TEXT,
    started_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    details JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Cron Jobs Table
CREATE TABLE IF NOT EXISTS cron_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    enabled BOOLEAN DEFAULT true,
    schedule_expr TEXT,
    timezone TEXT,
    session_target TEXT,
    wake_mode TEXT,
    payload_message TEXT,
    model TEXT,
    delivery_mode TEXT,
    delivery_channel TEXT,
    delivery_target TEXT,
    last_run_at TIMESTAMPTZ,
    last_status TEXT,
    last_duration_ms BIGINT,
    consecutive_errors INT DEFAULT 0,
    next_run_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. System Metrics Table
CREATE TABLE IF NOT EXISTS system_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    metric_name TEXT NOT NULL,
    metric_value JSONB NOT NULL,
    recorded_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Activity Log Table
CREATE TABLE IF NOT EXISTS activity_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_name TEXT,
    activity_type TEXT NOT NULL,
    description TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    recorded_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable Row Level Security (optional, disable for testing)
ALTER TABLE agent_status ENABLE ROW LEVEL SECURITY;
ALTER TABLE cron_jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE system_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE activity_log ENABLE ROW LEVEL SECURITY;

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_agent_status_agent_name ON agent_status(agent_name);
CREATE INDEX IF NOT EXISTS idx_agent_status_status ON agent_status(status);
CREATE INDEX IF NOT EXISTS idx_cron_jobs_job_id ON cron_jobs(job_id);
CREATE INDEX IF NOT EXISTS idx_cron_jobs_enabled ON cron_jobs(enabled);
CREATE INDEX IF NOT EXISTS idx_activity_log_recorded_at ON activity_log(recorded_at DESC);
CREATE INDEX IF NOT EXISTS idx_system_metrics_recorded_at ON system_metrics(recorded_at DESC);

-- Insert sample data (optional)
-- INSERT INTO agent_status (agent_name, status, task_name, details) 
-- VALUES ('main', 'working', 'Processing requests', '{"channel": "telegram"}');
