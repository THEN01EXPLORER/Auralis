# 🎬 Auralis Video Demo Guide

Quick guide to record a 3-minute demo video.

## Pre-Recording Setup
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Demo contract ready (demo-contracts/VulnerableBank.sol)
- [ ] GitHub demo repo URL ready
- [ ] Screen recording software installed (OBS Studio or Windows Game Bar)

## Demo Script (3 minutes)

### [0:00-0:30] Hook & Problem
**Show:** News about smart contract hacks
**Say:** "Smart contracts secure billions, but one vulnerability can cost millions. Traditional audits are slow and expensive."

### [0:30-1:30] Solution & Single Contract Demo
**Show:** Auralis interface
**Say:** "Auralis combines static analysis with AWS Bedrock AI."
**Do:** 
1. Paste vulnerable contract
2. Click "Analyze Contract"
3. Show results with risk scores
4. Click "Show Fix" to reveal remediation

### [1:30-2:30] Repository Scanner (Wow Feature)
**Show:** Repository scanner section
**Say:** "Analyze entire GitHub repositories at once."
**Do:**
1. Paste GitHub URL
2. Click "Analyze Repo"
3. Show tabbed results
4. Click through 2-3 file tabs

### [2:30-3:00] Close
**Show:** Architecture or results
**Say:** "Built on AWS Bedrock, Lambda, and Amplify. Try it at [your-url]."

## Recording Tips
- Use 1920x1080 resolution, 30fps
- Clear audio with good microphone
- Practice 2-3 times before recording
- Record multiple takes, pick the best

## Editing Checklist
- [ ] Add title card (0:00-0:03)
- [ ] Add end card with URL (2:57-3:00)
- [ ] Add subtle background music (optional)
- [ ] Export as MP4, 1080p
- [ ] Upload to YouTube

## Demo Repository
Create a small test repo with 2-3 vulnerable contracts, or use:
- OpenZeppelin contracts
- Your own test repo (recommended for control)

For detailed instructions, see original video guides in git history.
