# GitHub Actions Workflows

## Auralis PR Bot

The `auralis-pr-bot.yml` workflow automatically analyzes Solidity files in pull requests.

### Setup

1. **Set the API URL** (optional):
   - Go to: Settings > Secrets and variables > Actions > Variables
   - Click "New repository variable"
   - Name: `AURALIS_API_URL`
   - Value: Your Auralis API endpoint (e.g., `https://your-api.com`)
   - If not set, it will use a default placeholder

2. **The workflow will**:
   - Trigger on PRs that modify `.sol` files
   - Analyze changed contracts
   - Post a summary comment
   - Add inline comments on vulnerable lines

### Configuration

The workflow uses a placeholder API URL: `https://your-api-endpoint.com`

**To use your actual API:**
1. Edit `.github/workflows/auralis-pr-bot.yml`
2. Find line ~45: `AURALIS_API_URL: https://your-api-endpoint.com`
3. Replace with your actual endpoint
4. Commit and push

### How It Works

1. Checks out the code
2. Installs Python and Slither
3. Finds changed `.sol` files
4. Runs Auralis analysis
5. Posts results as PR comments
6. Adds inline suggestions

### Customization

Edit `.github/scripts/auralis_pr_analyzer.py` to customize the analysis logic.
