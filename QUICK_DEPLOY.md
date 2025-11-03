# Quick Deploy Commands

## Backend to AWS Lambda

```bash
cd backend
pip install -r requirements.txt
sam build
sam deploy --guided
```

**Note the API URL from output!**

## Frontend to AWS Amplify

### Update API URL
Edit `frontend/.env.production`:
```
REACT_APP_API_URL=https://[YOUR-API-ID].execute-api.us-east-1.amazonaws.com/Prod
```

### Build & Deploy
```bash
cd frontend
npm install
npm run build
```

Then:
1. Go to AWS Amplify Console
2. Click "Host web app"
3. Choose "Deploy without Git"
4. Drag & drop the `build` folder
5. Get your live URL!

## Test Your Live App

Visit: `https://[app-id].amplifyapp.com`

## Update Journal

Add to HACKATHON_JOURNAL.md:
```markdown
## Day 4 - Deployment ✅

**Live URLs:**
- Frontend: https://[app-id].amplifyapp.com
- Backend API: https://[api-id].execute-api.us-east-1.amazonaws.com/Prod

Deployed using AWS Lambda, API Gateway, and Amplify.
```

## Commit Changes

```bash
git add .
git commit -m "Day 4: Deployed Auralis to AWS Lambda and Amplify"
git push origin main
```

## Victory! 🎉

Your app is now live on the internet!
