# Vercel Deployment Guide

This guide will help you deploy the Notre Dame College Admission Portal to Vercel.

## Prerequisites

- Node.js installed on your machine
- Git repository (GitHub, GitLab, or Bitbucket)
- Vercel account (free at [vercel.com](https://vercel.com))

## Method 1: Deploy via Vercel CLI

### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

### Step 2: Login to Vercel

```bash
vercel login
```

Follow the prompts to authenticate with your Vercel account.

### Step 3: Deploy

Navigate to your project directory and run:

```bash
vercel --prod
```

The CLI will:

- Detect it's a Python project
- Build and deploy your application
- Provide you with a live URL

## Method 2: Deploy via GitHub (Recommended)

### Step 1: Push to GitHub

```bash
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

### Step 2: Connect to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Sign in with your GitHub account
3. Click "New Project"
4. Import your repository
5. Vercel will automatically detect the configuration

### Step 3: Configure (if needed)

Vercel should automatically:

- Detect the `vercel.json` configuration
- Install Python dependencies from `requirements.txt`
- Deploy the Flask app as serverless functions

## Project Structure for Vercel

The project has been restructured for Vercel deployment:

```
ndc-admission-results/
├── api/
│   └── index.py              # Main Flask app for Vercel
├── src/
│   ├── static/              # Static files (HTML, CSS, JS)
│   └── admission_data.json  # Admission data
├── vercel.json              # Vercel configuration
├── requirements.txt         # Python dependencies
└── package.json            # Project metadata
```

## Configuration Files

### vercel.json

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "15mb"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "/api/index.py"
    }
  ],
  "env": {
    "FLASK_ENV": "production"
  },
  "functions": {
    "api/index.py": {
      "maxDuration": 10
    }
  }
}
```

### requirements.txt (Simplified for Vercel)

```
Flask==3.1.1
flask-cors==6.0.0
Werkzeug==3.1.3
Jinja2==3.1.6
MarkupSafe==3.0.2
itsdangerous==2.2.0
click==8.2.1
blinker==1.9.0
```

## Environment Variables

Set these in your Vercel dashboard under Project Settings > Environment Variables:

- `FLASK_ENV`: `production`

## Custom Domain (Optional)

1. Go to your project dashboard on Vercel
2. Click on "Domains"
3. Add your custom domain
4. Follow the DNS configuration instructions

## Troubleshooting

### Common Issues

1. **Build Fails**

   - Check that `requirements.txt` only contains necessary packages
   - Ensure `api/index.py` is in the correct location

2. **Static Files Not Loading**

   - Verify the static folder path in `api/index.py`
   - Check that files exist in `src/static/`

3. **API Routes Not Working**

   - Ensure routes are properly defined in `api/index.py`
   - Check the `vercel.json` routing configuration

4. **Function Timeout**
   - Increase `maxDuration` in `vercel.json`
   - Optimize data loading functions

### Logs and Debugging

View deployment logs:

```bash
vercel logs [deployment-url]
```

Or check the Vercel dashboard for real-time logs.

## Performance Optimization

1. **Cold Start Optimization**

   - Keep the function lightweight
   - Cache admission data in memory
   - Use minimal dependencies

2. **Static Asset Optimization**
   - Compress images and CSS
   - Use CDN for external resources
   - Enable gzip compression

## Monitoring

Vercel provides built-in analytics:

- Function invocations
- Response times
- Error rates
- Bandwidth usage

Access these in your Vercel dashboard under "Analytics".

## Updating the Deployment

### Via Git (Automatic)

```bash
git add .
git commit -m "Update admission data"
git push origin main
```

Vercel will automatically redeploy.

### Via CLI

```bash
vercel --prod
```

## Cost Considerations

Vercel's free tier includes:

- 100GB bandwidth per month
- 100 serverless function invocations per day
- Automatic HTTPS
- Global CDN

For higher traffic, consider upgrading to a paid plan.

## Support

If you encounter issues:

1. Check Vercel's [documentation](https://vercel.com/docs)
2. Review the deployment logs
3. Contact Vercel support
4. Check the project's GitHub issues

---

**Happy Deploying! 🚀**
