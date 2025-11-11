# 🎥 Video Recording Guide - Day 4

**Goal:** Record a professional 3-minute demo video showcasing Auralis

---

## Pre-Recording Checklist

### Environment Setup
- [ ] **Quiet Location:** No background noise, echo, or interruptions
- [ ] **Good Lighting:** Natural light or desk lamp (avoid harsh shadows)
- [ ] **Clean Desktop:** Close all unnecessary applications and browser tabs
- [ ] **Hide Personal Info:** Remove any sensitive data from screen
- [ ] **Notifications Off:** Disable all system notifications (Windows, Slack, email)

### Software Setup
- [ ] **Screen Recorder Installed:** OBS Studio (recommended) or Windows Game Bar
- [ ] **Audio Tested:** Microphone working, no static or echo
- [ ] **Resolution Set:** 1920x1080 (Full HD)
- [ ] **Frame Rate:** 30fps minimum
- [ ] **Recording Area:** Full screen or application window

### Application Setup
- [ ] **Backend Running:** `uvicorn main:app --reload` in backend directory
- [ ] **Frontend Running:** `npm start` in frontend directory
- [ ] **Backend Tested:** Visit http://localhost:8000/health (should return {"status":"ok"})
- [ ] **Frontend Tested:** Visit http://localhost:3000 (should load Auralis UI)
- [ ] **Browser Cache Cleared:** Fresh start for clean demo
- [ ] **Browser Zoom:** Set to 100% (Ctrl+0)

### Demo Assets Ready
- [ ] **Vulnerable Contract:** Copy `demo-contracts/VulnerableBank.sol` to clipboard
- [ ] **GitHub URL:** Have a test repo URL ready (or use a public example)
- [ ] **Script Printed:** Have VIDEO_SCRIPT.md open on second monitor or printed

---

## Recording Software Setup

### Option 1: OBS Studio (Recommended)

**Download:** https://obsproject.com/

**Configuration:**
1. Open OBS Studio
2. Create new Scene: "Auralis Demo"
3. Add Source: "Display Capture" or "Window Capture" (browser)
4. Settings → Output:
   - Output Mode: Simple
   - Recording Quality: High Quality, Medium File Size
   - Recording Format: MP4
   - Encoder: x264
5. Settings → Video:
   - Base Resolution: 1920x1080
   - Output Resolution: 1920x1080
   - FPS: 30
6. Settings → Audio:
   - Sample Rate: 44.1kHz
   - Channels: Stereo
   - Desktop Audio: Disabled (no system sounds)
   - Mic/Auxiliary Audio: Your microphone

**Test Recording:**
- Click "Start Recording"
- Speak for 10 seconds
- Click "Stop Recording"
- Play back the video to check quality

### Option 2: Windows Game Bar (Built-in)

**Activation:**
1. Press `Win + G` to open Game Bar
2. Click the record button (or `Win + Alt + R`)
3. Speak to test audio
4. Stop recording (`Win + Alt + R` again)
5. Check video in Videos/Captures folder

**Settings:**
- Press `Win + I` → Gaming → Captures
- Video Quality: Standard (30fps) or High (60fps)
- Audio Quality: 192kbps
- Capture mouse cursor: Yes

---

## Recording Process

### Step 1: Practice Run (No Recording)
1. Open the script
2. Go through the entire demo flow
3. Time yourself (should be under 3 minutes)
4. Note any awkward transitions or timing issues
5. Practice 2-3 times until smooth

### Step 2: Warm-Up
1. Do vocal warm-ups (hum, tongue twisters)
2. Drink water (avoid milk/dairy before recording)
3. Take deep breaths to calm nerves
4. Smile (it affects your voice tone)

### Step 3: Record (Take 1)
1. Start screen recording
2. Wait 3 seconds (gives you room to trim)
3. Begin narration following the script
4. Perform all demo actions smoothly
5. If you make a mistake, pause, take a breath, and continue
6. End with 3 seconds of silence
7. Stop recording

### Step 4: Review Take 1
- Watch the entire video
- Check audio quality (clear, no background noise)
- Check video quality (smooth, no lag)
- Check timing (under 3 minutes)
- Note any mistakes or improvements needed

### Step 5: Record (Take 2 & 3)
- If Take 1 had issues, record again
- Try different pacing or emphasis
- Aim for 2-3 good takes to choose from

### Step 6: Select Best Take
- Watch all takes
- Choose the one with:
  - Best audio quality
  - Smoothest demo flow
  - Most natural narration
  - Best timing

---

## Demo Flow Breakdown

### [0:00-0:15] Hook
**Screen:** Show browser with news articles about smart contract hacks (optional: prepare screenshots)
**Action:** None (just narration over visuals)
**Narration:** "Smart contracts secure billions of dollars in cryptocurrency..."

### [0:15-0:45] Problem Statement
**Screen:** Show traditional audit process or just Auralis empty state
**Action:** None (just narration)
**Narration:** "Traditional security audits are slow, expensive..."

### [0:45-1:15] Solution
**Screen:** Show Auralis interface (empty state)
**Action:** None (just narration)
**Narration:** "Auralis is a hybrid smart contract security auditor..."

### [1:15-1:30] Paste Contract
**Screen:** Auralis code editor
**Action:** 
1. Click in code editor
2. Paste VulnerableBank.sol contract
3. Let it appear on screen for 2-3 seconds
**Narration:** "Let me show you. Here's a simple Ethereum contract..."

### [1:30-1:45] Run Analysis
**Screen:** Code editor with contract
**Action:**
1. Click "Analyze Contract" button
2. Show loading spinner
**Narration:** "Click Analyze. Within seconds, Auralis identifies..."

### [1:45-2:00] Show Results
**Screen:** Vulnerability report with results
**Action:**
1. Scroll through vulnerabilities
2. Point cursor at source badges (Static/AI/Hybrid)
3. Point at confidence scores
**Narration:** "Each vulnerability shows its detection source..."

### [2:00-2:15] Show Fix Feature
**Screen:** Vulnerability report
**Action:**
1. Click "Show Fix" button on a vulnerability
2. Scroll through remediation explanation
3. Show code example
**Narration:** "But here's the game-changer. Click 'Show Fix'..."

### [2:15-2:45] Repository Scanner
**Screen:** Auralis interface
**Action:**
1. Scroll down to "Analyze GitHub Repository" section
2. Paste GitHub URL in input field
3. Click "Analyze Repo" button
4. Show loading state
5. Show results with tabs
6. Click through 2-3 file tabs
7. Show vulnerability counts on tabs
**Narration:** "And here's where it gets even better. Paste a GitHub repository URL..."

### [2:45-3:00] Call to Action
**Screen:** Show architecture diagram (optional) or just results
**Action:** None (just narration)
**Narration:** "Auralis makes smart contract security accessible..."

---

## Common Mistakes to Avoid

❌ **Speaking too fast:** Slow down, enunciate clearly
❌ **Dead air:** Keep narration flowing, no long pauses
❌ **Mouse wandering:** Keep cursor purposeful, don't fidget
❌ **Clicking too fast:** Let UI animations complete
❌ **Forgetting to show features:** Follow the script checklist
❌ **Going over time:** Practice timing, cut unnecessary parts
❌ **Background noise:** Record in quiet environment
❌ **Low energy:** Sound enthusiastic but professional

---

## Audio Tips

✅ **Microphone Position:** 6-8 inches from mouth, slightly off to side
✅ **Volume:** Speak at normal conversation volume
✅ **Pacing:** Moderate speed, clear enunciation
✅ **Tone:** Enthusiastic but professional, not monotone
✅ **Breathing:** Take breaths at natural pauses, not mid-sentence
✅ **Plosives:** Avoid "p" and "b" sounds directly into mic (use pop filter or angle mic)

---

## Video Quality Checklist

Before finalizing your recording, verify:

- [ ] **Resolution:** 1920x1080 (Full HD)
- [ ] **Frame Rate:** 30fps minimum (smooth playback)
- [ ] **Audio Quality:** Clear voice, no background noise
- [ ] **Video Quality:** No lag, stuttering, or pixelation
- [ ] **Timing:** Under 3 minutes (ideally 2:45-2:55)
- [ ] **Content:** All features shown (code editor, repo scanner, show fix)
- [ ] **Cursor:** Visible and purposeful
- [ ] **UI:** All text readable, no cut-off elements
- [ ] **Transitions:** Smooth, no jarring jumps

---

## Backup Plan

If recording doesn't go well:
1. **Take a break:** Walk away for 10 minutes
2. **Simplify:** Focus on core features only
3. **Shorter version:** Use 1-minute alternative script
4. **Screen + Voiceover:** Record screen first, add voice later
5. **Ask for help:** Have someone else narrate while you drive UI

---

## Next Steps After Recording

Once you have a good take:
1. Save the raw video file
2. Note the filename and location
3. Move to Day 5: Video Editing
4. Don't delete any takes until final video is complete

---

## Emergency Troubleshooting

**Problem:** Audio is too quiet
**Solution:** Increase mic gain in Windows settings or OBS

**Problem:** Video is laggy
**Solution:** Close other applications, reduce recording quality, or use window capture instead of display capture

**Problem:** Backend/Frontend not responding
**Solution:** Restart both servers, check logs for errors

**Problem:** Can't remember script
**Solution:** Record in segments, edit together later

**Problem:** Nervous/anxious
**Solution:** Remember, you can record multiple takes. No one sees the mistakes.

---

**You've got this! The hard work is done. Now just show it off.** 🎬
