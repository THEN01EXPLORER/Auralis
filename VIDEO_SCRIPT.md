# 🎬 Auralis Demo Video Script

**Duration:** 3 minutes
**Target Audience:** Hackathon judges, developers, blockchain enthusiasts

---

## Script with Timing

### [0:00-0:15] HOOK - The Problem
**Visual:** Show news headlines about smart contract hacks
**Narration:**
> "Smart contracts secure billions of dollars in cryptocurrency. But one vulnerability can cost millions. The DAO hack: $60 million. Parity wallet: $150 million. These weren't theoretical risks—they were real disasters."

---

### [0:15-0:45] PROBLEM STATEMENT
**Visual:** Show traditional audit process (slow, expensive)
**Narration:**
> "Traditional security audits are slow, expensive, and often miss critical issues. Automated tools generate too many false positives. Developers need something better: fast, accurate, and actionable security insights. That's why I built Auralis."

---

### [0:45-1:15] SOLUTION - Introducing Auralis
**Visual:** Show Auralis logo and interface
**Narration:**
> "Auralis is a hybrid smart contract security auditor. It combines traditional static analysis with AWS Bedrock's AI capabilities. Static analysis catches known patterns instantly. AI understands context and finds subtle vulnerabilities. Together, they provide comprehensive coverage with intelligent insights."

---

### [1:15-2:30] DEMO - Show Don't Tell
**Visual:** Live demo of the application

**[1:15-1:30] Paste Contract**
**Narration:**
> "Let me show you. Here's a simple Ethereum contract with a classic vulnerability."
**Action:** Paste vulnerable bank contract

**[1:30-1:50] Run Analysis**
**Narration:**
> "Click Analyze. Within seconds, Auralis identifies multiple vulnerabilities. See the risk score? 75 out of 100—this contract is dangerous."
**Action:** Click Analyze button, show results loading

**[1:50-2:10] Show Results**
**Narration:**
> "Each vulnerability shows its detection source. This reentrancy issue was found by both static analysis AND AI—that's why it's marked 'Hybrid' with 95% confidence."
**Action:** Point to source badges and confidence scores

**[2:10-2:30] Show Fix Feature**
**Narration:**
> "But here's the game-changer. Click 'Show Fix.' Auralis doesn't just find bugs—it shows you exactly how to fix them. Detailed explanation, working code example, best practices. This is what developers actually need."
**Action:** Click Show Fix button, scroll through remediation

---

### [2:30-3:00] IMPACT & CALL TO ACTION
**Visual:** Show architecture diagram, AWS logos
**Narration:**
> "Auralis makes smart contract security accessible to every developer. Fast analysis. Clear insights. Actionable fixes. Built entirely on AWS: Bedrock for AI, Lambda for compute, Amplify for hosting. This is the future of blockchain security—and it's available now."

**Visual:** Show live URL
**Narration:**
> "Try it yourself at [your-url]. Securing the future of blockchain, one contract at a time."

---

## Recording Notes

### Equipment Needed
- Screen recording software (OBS Studio, Loom, or built-in)
- Microphone (or clear laptop mic)
- Quiet environment

### Recording Tips
1. **Practice first:** Run through 2-3 times before recording
2. **Speak clearly:** Enunciate, moderate pace
3. **Show, don't tell:** Let the UI speak for itself
4. **Keep energy up:** Sound enthusiastic but professional
5. **Edit ruthlessly:** Cut any dead air or mistakes

### Screen Recording Setup
- Resolution: 1920x1080 (Full HD)
- Frame rate: 30fps minimum
- Audio: 44.1kHz, clear voice
- Format: MP4 (H.264)

### Demo Preparation
1. Clear browser cache
2. Have contract code ready to paste
3. Backend running and tested
4. Frontend loaded and ready
5. Close unnecessary tabs/windows
6. Hide personal information

---

## B-Roll Footage (Optional)

If you have time, capture these additional clips:
- Empty state (welcome screen)
- Loading animation
- Error state
- Different vulnerability types
- Mobile responsive view

---

## Editing Checklist

- [ ] Trim beginning/end
- [ ] Add title card (0:00-0:03)
- [ ] Add background music (subtle, low volume)
- [ ] Add text overlays for key points
- [ ] Add zoom/highlight for important UI elements
- [ ] Add end card with URL and GitHub link
- [ ] Export in 1080p
- [ ] Test playback before uploading

---

## Alternative: Shorter Version (1 minute)

If 3 minutes is too long:

**[0:00-0:15]** Hook + Problem
**[0:15-0:30]** Solution (Auralis intro)
**[0:30-0:50]** Quick demo (analyze + show fix)
**[0:50-1:00]** Impact + URL

---

## Upload Destinations

1. **YouTube** (primary)
   - Title: "Auralis - AI-Powered Smart Contract Security Auditor"
   - Description: Include GitHub link, live demo URL
   - Tags: blockchain, security, AWS, Bedrock, smart contracts

2. **Hackathon Platform** (required)
   - Follow submission guidelines
   - Include video link in submission form

3. **GitHub README** (embedded)
   - Add YouTube embed code
   - Or link to video

---

## Sample Contract for Demo

Use this contract in the video:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VulnerableBank {
    mapping(address => uint) public balances;
    
    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }
    
    function withdraw(uint amount) public {
        require(balances[msg.sender] >= amount);
        (bool success, ) = msg.sender.call{value: amount}("");
        balances[msg.sender] -= amount;
    }
}
```

---

## Key Messages to Emphasize

1. **Hybrid = Better:** Static + AI is more powerful than either alone
2. **Actionable:** Not just detection, but remediation
3. **AWS-Powered:** Built on enterprise-grade infrastructure
4. **Developer-Friendly:** Fast, clear, easy to use
5. **Real Impact:** Prevents real financial losses

---

## Final Checklist

- [ ] Script memorized/practiced
- [ ] Demo environment ready
- [ ] Recording software tested
- [ ] Audio quality checked
- [ ] Contract code ready to paste
- [ ] Backend running smoothly
- [ ] Frontend loaded and tested
- [ ] Timing practiced (under 3 min)
- [ ] Backup recording made
- [ ] Video edited and exported
- [ ] Uploaded to YouTube
- [ ] Link added to submission

---

**You've got this! Practice makes perfect. Record, review, refine.** 🎬
