# 📸 Screenshot Checklist for Final Submission

## Required Screenshots

### 1. Empty State (Welcome Screen)
**How to capture:**
- Start both backend and frontend servers
- Open app in browser (http://localhost:3000)
- Take screenshot BEFORE clicking Analyze
- Should show: Shield icon, welcome message, feature highlights

**What to show:**
- 🛡️ Shield icon with pulse animation
- "Auralis is ready to secure your code"
- Three feature badges (AI-Powered, Real-Time, Smart Remediation)

**Save as:** `screenshots/01-empty-state.png`

---

### 2. Success State (Full Analysis Report)
**How to capture:**
- Paste a vulnerable contract in the editor
- Click "Analyze Contract"
- Wait for analysis to complete
- Take screenshot of the full report

**What to show:**
- Risk Score meter
- Analysis Type: "Hybrid" (or "Static")
- Processing Time: "XXXms"
- Vulnerability list with source badges [Static]/[AI]/[Hybrid]
- At least 2-3 vulnerabilities visible

**Save as:** `screenshots/02-success-state.png`

---

### 3. Show Fix Feature (Expanded Remediation)
**How to capture:**
- From the success state above
- Click on a vulnerability to expand it
- Click the "▶ Show Fix" button
- Take screenshot showing the expanded remediation

**What to show:**
- "▼ Hide Fix" button (showing it's expanded)
- 🔧 How to Fix section
- Remediation explanation text
- Fixed Code block with syntax

**Save as:** `screenshots/03-show-fix-expanded.png`

---

### 4. Error State (Graceful Failure)
**How to capture:**
- STOP the backend server (Ctrl+C in backend terminal)
- In the frontend, click "Analyze Contract" again
- Take screenshot of the error message

**What to show:**
- ⚠️ Warning icon
- "Analysis Failed" heading
- Error message: "Cannot connect to backend..."
- Helpful hint text
- Red border around error panel

**Save as:** `screenshots/04-error-state.png`

---

### 5. Source Badge Close-Up (Optional but Impressive)
**How to capture:**
- Zoom in on a vulnerability card
- Show the source badge clearly ([Static], [AI], or [Hybrid])

**What to show:**
- Clear view of the source badge with icon
- Confidence percentage
- Line number with 🔍 icon

**Save as:** `screenshots/05-source-badge-detail.png`

---

### 6. Analysis Metadata Close-Up (Optional)
**How to capture:**
- Zoom in on the metadata section
- Show Analysis Type and Processing Time clearly

**What to show:**
- "ANALYSIS TYPE" label with value
- "PROCESSING TIME" label with milliseconds
- Clean, professional styling

**Save as:** `screenshots/06-metadata-detail.png`

---

## Screenshot Tips

### Quality:
- Use full browser window (not just a small window)
- Clear, high-resolution (at least 1920x1080)
- Good contrast and readable text
- No personal information visible

### Browser:
- Use Chrome or Edge for best rendering
- Hide browser dev tools before capturing
- Consider using full-screen mode (F11)

### Lighting:
- Use a dark theme (already set in app)
- Ensure text is crisp and readable
- No glare or reflections

### Tools:
- Windows: Win+Shift+S (Snipping Tool)
- Or use browser screenshot extensions
- Save as PNG (not JPG) for better quality

---

## After Capturing

1. Review each screenshot for quality
2. Rename files according to the naming scheme above
3. Move to `screenshots/` folder
4. Update README.md to reference these images
5. Commit and push to GitHub:
   ```bash
   git add screenshots/
   git commit -m "docs: Add final application screenshots"
   git push
   ```

---

## Usage in Documentation

These screenshots will be used in:
- README.md (main project page)
- Hackathon submission form
- Demo video (as B-roll)
- Social media posts (if sharing)

**Make them count! These are your "proof of work" for the judges. 📸**
