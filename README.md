# 🌸 Anime Office Command Center 🌸

<p align="center">
  <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Sakura&backgroundColor=ffeaa7" width="100" />
  <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Yuki&backgroundColor=dfe6e9" width="100" />
  <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Hana&backgroundColor=fab1a0" width="100" />
</p>

A kawaii anime-style dashboard to monitor your agents like cute anime employees working in an office! Watch your agents as adorable anime characters at their desks. ✨

## ✨ Features

- 🌸 **Cute Anime Employee Avatars** - Watch your agents as kawaii anime characters!
- 🏢 **Office Scene Background** - Immersive anime office environment
- ⚙️ **Cron Job Monitoring** - Track scheduled tasks at a glance
- 🔄 **Real-time Updates** - Auto-refresh with configurable intervals
- 🎨 **Pastel Color Palette** - Soft, relaxing kawaii aesthetic
- 🎮 **Interactive Elements** - Buttons to call meetings, coffee breaks, and more!

## 🚀 Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Docker

```bash
# Build and run
docker build -t anime-office .
docker run -p 8501:8501 anime-office
```

## ☁️ Deployment

### Streamlit Cloud

1. Push this code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy! 

### Zeabur

1. Push this code to GitHub
2. Log in to [zeabur.com](https://zeabur.com)
3. Create new project → Add service → Streamlit
4. Connect your GitHub repository
5. Done! 🎉

## 🎭 Customizing Employees

Edit the `EMPLOYEES` list in `app.py` to add your own agents:

```python
{
    "name": "YourAgent",
    "role": "Custom Role",
    "emoji": "🎭",
    "color": "#FFB6C1",
    "status": "active",
    "task": "Doing stuff",
    "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=YourAgent",
    "quote": "Your quote here!"
}
```

## 📝 License

MIT License - Feel free to use and modify!

---

<p align="center">
  Made with 💕 and ☕ | Working hard or hardly working? Both! ✨
</p>
