
# 🐳 Docker Quick Start Guide

## Prerequisites
- Docker Desktop installed on your system
- Your AbacusAI API key ([Get one here](https://abacus.ai/))

## 🚀 Quick Deploy (5 minutes)

### Step 1: Get the Application
```bash
# Clone or download the application
git clone <repository-url> research_summary_app
cd research_summary_app
```

### Step 2: Configure Environment
```bash
# Copy the environment template
cp .env.docker-example .env

# Edit with your API key
nano .env  # or use your preferred editor
```

### Step 3: Set Your API Key
```bash
# In the .env file, replace:
ABACUSAI_API_KEY=your_actual_api_key_here
```

### Step 4: Deploy
```bash
# Build and run
docker-compose up -d --build

# Check status
docker-compose ps
```

### Step 5: Access
Open your browser to: `http://localhost:8501`

## 📋 Common Commands

```bash
# View logs
docker-compose logs -f

# Stop application
docker-compose down

# Restart application
docker-compose restart

# Update application
git pull
docker-compose down
docker-compose up -d --build
```

## 🔧 Troubleshooting

**Port 8501 in use?**
```bash
# Use different port
# Edit docker-compose.yml: "8502:8501"
```

**Container won't start?**
```bash
# Check logs
docker-compose logs research-app

# Verify API key
cat .env
```

**Need help?**
- Check the full deployment guide: `docs/deployment.md`
- Review the main README: `README.md`

## 🎯 What You Get

✅ **Multi-AI Models**: GPT-4, Claude, Deepseek, Llama, Mistral  
✅ **Easy Upload**: BibTeX and PDF file support  
✅ **Smart Summaries**: Multiple prompt templates  
✅ **Quality Evaluation**: Rating and feedback system  
✅ **Analytics Dashboard**: Performance insights  
✅ **Data Persistence**: Your data is automatically saved  

## 🔒 Security Notes

- Keep your `.env` file secure
- Never commit API keys to version control
- Your data stays on your machine
- Application runs in isolated container

---

**Ready to get started? Run the 5-minute quick deploy above!**
