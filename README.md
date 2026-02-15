# 🌸 Anime Office Command Center 🌸

<p align="center">
  <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Sakura&backgroundColor=ffeaa7" width="100" />
  <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Yuki&backgroundColor=dfe6e9" width="100" />
  <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Hana&backgroundColor=fab1a0" width="100" />
</p>

A kawaii anime-style dashboard to monitor your OpenClaw agents like cute anime employees working in an office! Now with **REAL data** from OpenClaw and Supabase! ✨

## ✨ Features

- 🌸 **Cute Anime Employee Avatars** - Watch your agents as kawaii anime characters!
- 🏢 **Office Scene Background** - Immersive anime office environment
- ⚙️ **Cron Job Monitoring** - Track scheduled tasks at a glance
- 🔄 **Real-time Updates** - Auto-refresh with configurable intervals
- 🎨 **Pastel Color Palette** - Soft, relaxing kawaii aesthetic
- 🎮 **Interactive Elements** - Buttons to call meetings, coffee breaks, and more!
- 📡 **Live OpenClaw Integration** - Reads real session and cron data from OpenClaw
- ☁️ **Supabase Backend** - Optional cloud sync for multi-device monitoring

## 🚀 Quick Start

### 1. Set Up Supabase (Optional but Recommended)

```bash
# Copy the example env file
cp .env.example .env

# Edit .env with your Supabase credentials
# Get them from: https://app.supabase.com/project/_/settings/api
```

Run the SQL schema in Supabase:
```bash
# Copy the contents of supabase_schema.sql and run in Supabase SQL Editor
```

### 2. Install & Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### 3. Start the Sync Daemon (Optional)

To sync data to Supabase every 30 seconds:
```bash
python sync_agent.py
```

### Docker

```bash
# Build and run
docker build -t anime-office .
docker run -p 8501:8501 -e SUPABASE_URL=xxx -e SUPABASE_KEY=xxx anime-office
```

## ☁️ Deployment

### Streamlit Cloud

1. Push this code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Add secrets: `SUPABASE_URL` and `SUPABASE_KEY`
5. Deploy! 

### Zeabur

1. Push this code to GitHub
2. Log in to [zeabur.com](https://zeabur.com)
3. Create new project → Add service → Streamlit
4. Add environment variables in Zeabur settings
5. Connect your GitHub repository
6. Done! 🎉

## 📊 Data Sources

### Primary: OpenClaw Filesystem
The dashboard reads directly from OpenClaw's session and cron files:
- `/home/node/.openclaw/agents/main/sessions/sessions.json`
- `/home/node/.openclaw/cron/jobs.json`

### Optional: Supabase Cloud
When configured, data is synced to Supabase for:
- Historical tracking
- Multi-device access
- Activity logging

## 🎭 How It Works

1. **Agent Status**: Reads from OpenClaw sessions, determines if agents are working/idle based on last update time
2. **Cron Jobs**: Shows all scheduled jobs with their status (running/pending/stopped)
3. **Sync Daemon**: Background script that syncs data to Supabase every 30 seconds

## 📝 License

MIT License - Feel free to use and modify!

---

<p align="center">
  Made with 💕 and ☕ | Working hard or hardly working? Both! ✨
</p>
