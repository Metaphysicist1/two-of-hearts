# 💝 Valentine's Day Invitation Creator

A beautiful, modern web application for creating personalized Valentine's Day invitations with custom themes, photos, and heartfelt messages.

## 🚀 Deploy to GitHub Pages

Follow these steps to host your own version on GitHub Pages:

### Method 1: Using GitHub Web Interface (Easiest)

1. **Create a GitHub Account** (if you don't have one)
   - Go to [github.com](https://github.com)
   - Click "Sign up" and follow the steps

2. **Create a New Repository**
   - Click the "+" icon in the top right corner
   - Select "New repository"
   - Name it: `valentine-invitation` (or any name you like)
   - Make it **Public**
   - ✅ Check "Add a README file"
   - Click "Create repository"

3. **Upload Your Files**
   - Click "Add file" → "Upload files"
   - Drag and drop these files:
     - `index.html` (rename `index-modern-modified.html` to `index.html`)
     - `viewer-modern.html`
   - Click "Commit changes"

4. **Enable GitHub Pages**
   - Go to repository Settings (gear icon)
   - Scroll down to "Pages" in the left sidebar
   - Under "Source", select "Deploy from a branch"
   - Select branch: `main` (or `master`)
   - Select folder: `/ (root)`
   - Click "Save"

5. **Access Your Site**
   - Wait 1-2 minutes for deployment
   - Your site will be live at: `https://YOUR-USERNAME.github.io/valentine-invitation/`
   - Example: `https://johnsmith.github.io/valentine-invitation/`

### Method 2: Using Git (For Developers)

```bash
# 1. Create a new folder and navigate to it
mkdir valentine-invitation
cd valentine-invitation

# 2. Initialize git repository
git init

# 3. Copy your HTML files here
# - Rename index-modern-modified.html to index.html
# - Copy viewer-modern.html

# 4. Add files to git
git add .
git commit -m "Initial commit: Valentine's Invitation Creator"

# 5. Create a new repository on GitHub (via web interface)
# Then connect your local repo to GitHub:

git remote add origin https://github.com/YOUR-USERNAME/valentine-invitation.git
git branch -M main
git push -u origin main

# 6. Enable GitHub Pages in repository settings
```

### Method 3: Custom Domain (Optional)

If you want a custom domain like `valentines.yourdomain.com`:

1. In your repository, create a file named `CNAME`
2. Add your custom domain inside: `valentines.yourdomain.com`
3. In your domain registrar, add a CNAME record pointing to: `YOUR-USERNAME.github.io`

## 📁 Required Files

Make sure you have these files in your repository:

```
valentine-invitation/
├── index.html              (your main form - rename from index-modern-modified.html)
├── viewer-modern.html      (the invitation display page)
└── README.md              (this file - optional)
```

## 🎨 Features

- ✨ Beautiful glassmorphism design
- 💕 4 theme options (Romantic, Playful, Elegant, Minimalist)
- 📸 Photo upload support
- 💌 Custom messages with character counter
- 🎭 Live preview
- 📱 Fully responsive
- 🌈 Animated particle background
- 📋 Easy sharing via link

## 🔧 Customization

You can customize colors by editing the CSS variables in `index.html`:

```css
:root {
  --primary: #ff1493;      /* Main pink color */
  --secondary: #ff69b4;    /* Secondary pink */
  --accent: #ffd700;       /* Gold accent */
}
```

## 📝 How to Use

1. Visit your deployed site
2. Fill in the recipient's name
3. Add your name (optional)
4. Upload a photo (optional)
5. Choose a theme
6. Write your message
7. Click "Preview" to see it
8. Click "Generate & Share" to create a shareable link

## 🐛 Troubleshooting

**Site not showing up?**
- Wait 2-3 minutes after enabling GitHub Pages
- Check that files are named correctly (`index.html` not `index-modern-modified.html`)
- Ensure repository is Public, not Private

**Photos not working?**
- Photos are stored in browser sessionStorage
- Works best when sharing within the same browser session
- For permanent hosting, consider adding a backend

**Can't edit after deployment?**
- To update: Upload new files via GitHub web interface
- Or use Git to push changes: `git add . && git commit -m "Update" && git push`

## 📱 Sharing

After generating an invitation, users can:
- Copy the URL from the browser
- Share via social media, email, or messaging apps
- The invitation opens in any web browser

## 🎉 Multiple Projects

Want to create different invitation sites?

1. Create multiple repositories:
   - `valentine-invitation` → yourname.github.io/valentine-invitation
   - `birthday-invitation` → yourname.github.io/birthday-invitation
   - `wedding-invitation` → yourname.github.io/wedding-invitation

2. Each will have its own unique URL!

## 📜 License

Free to use and modify for personal and commercial projects.

## 💖 Credits

Created with love using HTML, CSS, and JavaScript.
No frameworks, no dependencies, just pure vanilla code!

---

**Enjoy spreading love! 💝**

For questions or issues, open an issue on GitHub.
# valentine-invitation
# two-of-hearts
