# Spider-Run Game - File Download Server

## 🚀 Deployment to Vercel

Your Spider-Run game is now configured as a **file download server** for Vercel deployment!

### 📁 Files Created for Vercel:

1. **`app.py`** - File download server entry point for Vercel
2. **`vercel.json`** - Vercel configuration
3. **`requirements.txt`** - Python dependencies (updated for file serving)
4. **`runtime.txt`** - Python version specification
5. **`.vercelignore`** - Files to exclude from deployment
6. **`DEPLOYMENT.md`** - This deployment guide

### 🛠️ Deployment Steps:

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy to Vercel**:
   ```bash
   vercel
   ```

4. **Follow the prompts**:
   - Link to existing project or create new
   - Confirm deployment settings
   - Wait for build and deployment

### ✅ Pre-deployment Checklist:

- [x] File download server properly configured
- [x] ZIP file creation functionality
- [x] All dependencies listed in requirements.txt
- [x] Python version specified
- [x] Vercel configuration complete

### 📦 Download Options:

After deployment, users can download:

1. **Complete Game** (`/download/game`)
   - All game files, assets, and documentation
   - Ready-to-run package

2. **Assets Only** (`/download/static`)
   - Game images, sounds, and media files
   - For users who want just the assets

3. **Source Code** (`/download/source`)
   - Python source code and configuration files
   - For developers

4. **Documentation** (`/download/docs`)
   - Game design documents and guides
   - For reference

### 🎮 Game Features (in downloaded files):

- **Two Complete Levels**: East Village (Level 1) and Times Square (Level 2)
- **6 Villains**: Doc Ock, Green Goblin, Vulture, Venom, Mysterio, Electro
- **Special Powers**: Each villain has unique abilities
- **Interactive Elements**: Web shooters, taxis, bombs, crashes
- **Comic Book Cutscenes**: Story-driven narrative
- **Background Music**: Level-specific audio
- **Responsive Design**: Works on different screen sizes

### 🔧 Troubleshooting:

If deployment fails:

1. **Check Vercel logs** for specific errors
2. **Verify Python version** matches runtime.txt
3. **Ensure all static files** are in the static/ directory
4. **Check file permissions** for ZIP creation

### 🌐 Post-Deployment:

After successful deployment, your download server will be available at:
`https://your-project-name.vercel.app`

Users can:
- Visit the main page to see download options
- Click download buttons to get ZIP files
- Extract and run the game locally

### 📝 Notes:

- The server creates ZIP files on-demand
- All downloads include proper file structure
- Users can run the game locally after downloading
- Compatible with Vercel's serverless architecture

🎉 **Your Spider-Run game download server is ready for the web!**
