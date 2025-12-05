# Frontend Dashboard

React-based web dashboard for the DevOps Security Research Project.

## Features

- **React 18** - Modern React with hooks
- **Vite** - Lightning-fast build tool
- **React Router** - Client-side routing
- **Responsive Design** - Mobile-friendly interface
- **API Integration** - Connects to backend and Python services
- **Real-time Monitoring** - System health indicators
- **Security Metrics** - Comprehensive security dashboard

## Tech Stack

- **Framework:** React 18
- **Build Tool:** Vite
- **Routing:** React Router v6
- **HTTP Client:** Axios
- **Testing:** Vitest + React Testing Library
- **Server:** Nginx (production)

## Prerequisites

- Node.js >= 18.0.0
- npm >= 9.0.0
- Backend API running on port 3000 (optional)
- Python service running on port 8000 (optional)

## Getting Started

### Local Development

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

   The app will be available at `http://localhost:3001`

3. **Build for production:**
   ```bash
   npm run build
   ```

4. **Preview production build:**
   ```bash
   npm run preview
   ```

### Running Tests

```bash
# Run tests once
npm test

# Run tests with UI
npm run test:ui

# Run tests with coverage
npm run test:coverage
```

### Code Quality

```bash
# Lint code
npm run lint

# Fix linting issues
npm run lint:fix

# Format code with Prettier
npm run format
```

## Application Structure

```
frontend/
├── public/                  # Static assets
├── src/
│   ├── components/          # React components
│   │   ├── Dashboard.jsx    # Main dashboard
│   │   ├── Users.jsx        # User management
│   │   ├── DataProcessing.jsx  # Data processing interface
│   │   └── SecurityMetrics.jsx # Security dashboard
│   ├── tests/               # Test files
│   ├── App.jsx              # Main app component
│   ├── main.jsx             # Entry point
│   └── index.css            # Global styles
├── Dockerfile
├── nginx.conf               # Nginx configuration
├── vite.config.js
└── package.json
```

## Pages

### Dashboard (`/`)
- System overview with statistics
- Total users, data processed, security scans
- Project information and architecture
- Service health indicators

### Users API (`/users`)
- View all users from backend API
- Create new users
- Interact with Node.js backend

### Data Processing (`/processing`)
- Single value processing
- Batch data processing
- Analytics summary
- Python service integration

### Security Metrics (`/security`)
- Security scan statistics
- Active security tools (15+)
- Vulnerability distribution
- ML feature categories

## API Integration

### Backend API (Node.js)
```
Base URL: http://localhost:3000/api/v1
Endpoints:
  GET  /users
  POST /users
  GET  /users/:id
```

### Python Service (FastAPI)
```
Base URL: http://localhost:8000/api/v1
Endpoints:
  POST /process
  POST /batch-process
  GET  /analytics/summary
```

## Docker

### Build Image

```bash
docker build -t frontend:latest .
```

### Run Container

```bash
docker run -p 80:80 frontend:latest
```

The application uses a multi-stage build:
1. **Builder stage** - Build React app with Vite
2. **Production stage** - Serve with Nginx

## Kubernetes Deployment

### Deploy to Kubernetes

```bash
kubectl apply -f k8s/deployment.yaml
```

### Verify Deployment

```bash
kubectl get pods -n production -l app=frontend
kubectl get svc -n production frontend
kubectl get ingress -n production frontend
```

### Access Application

```bash
# Port forward to local machine
kubectl port-forward -n production svc/frontend 8080:80

# Or access via Ingress (if configured)
http://devops-dashboard.local
```

## Production Configuration

### Nginx Features

- **Security Headers** - XSS protection, frame options
- **Gzip Compression** - Reduced bandwidth
- **Static Asset Caching** - 1-year cache for assets
- **SPA Routing** - Fallback to index.html
- **API Proxying** - Proxy to backend services
- **Health Check** - `/health` endpoint

### Environment Variables

None required - all configuration is build-time.

For different API URLs, modify `vite.config.js`:

```javascript
server: {
  proxy: {
    '/api': {
      target: 'https://your-backend-api.com',
      changeOrigin: true,
    },
  },
},
```

## Development

### Adding a New Page

1. Create component in `src/components/NewPage.jsx`
2. Add route in `src/App.jsx`:
   ```jsx
   <Route path="/new-page" element={<NewPage />} />
   ```
3. Add navigation link in `App.jsx`
4. Create CSS file `src/components/NewPage.css`
5. Write tests `src/components/NewPage.test.jsx`

### Component Structure

```jsx
import { useState, useEffect } from 'react'
import './ComponentName.css'

function ComponentName() {
  const [data, setData] = useState(null)

  useEffect(() => {
    // Fetch data
  }, [])

  return (
    <div className="ComponentName">
      {/* JSX */}
    </div>
  )
}

export default ComponentName
```

## CI/CD Pipeline

The frontend includes a comprehensive GitHub Actions workflow (`.github/workflows/ci-cd.yml`) with 10 stages:

### Pipeline Stages

1. **Code Quality** - ESLint and Prettier checks
2. **Testing** - Vitest unit tests with 70% coverage requirement
3. **Secret Scanning** - TruffleHog and Gitleaks for credential detection
4. **SAST** - CodeQL and Semgrep static analysis
5. **Dependency Scanning** - npm audit and Snyk vulnerability detection
6. **Build** - Production bundle build and Docker image creation
7. **Container Scanning** - Trivy, Grype, and Dockle security scans
8. **Push Image** - Push to GitHub Container Registry (main branch only)
9. **Deploy** - Deploy to Kubernetes via ArgoCD GitOps
10. **Collect Metrics** - Aggregate security scan results for research

### Pipeline Features

- **SARIF Upload** - Security results uploaded to GitHub Security tab
- **Artifact Retention** - 90-day retention for research data collection
- **Matrix Strategy** - Parallel execution of security scanners
- **Caching** - npm and Docker layer caching for faster builds
- **SBOM & Provenance** - Software Bill of Materials generation
- **Auto-deployment** - GitOps deployment on main branch push

### Triggering the Pipeline

```bash
# Automatic triggers
git push origin main          # Full pipeline with deployment
git push origin develop       # Full pipeline without deployment
git push origin feature/*     # On pull request to main

# Manual trigger (if configured)
gh workflow run ci-cd.yml
```

## Performance

### Lighthouse Scores (Target)

- **Performance:** 90+
- **Accessibility:** 95+
- **Best Practices:** 95+
- **SEO:** 90+

### Optimizations

- Code splitting (React.lazy)
- Image optimization
- Gzip compression
- Static asset caching
- Minified bundles

## Browser Support

- Chrome (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Edge (latest 2 versions)

## Security

- ✅ Security headers (CSP, X-Frame-Options)
- ✅ No sensitive data in client code
- ✅ HTTPS in production (recommended)
- ✅ Dependency scanning
- ✅ Non-root Docker user
- ✅ Read-only root filesystem

## Troubleshooting

### Issue: API calls fail

**Solution:** Ensure backend services are running:
```bash
# Backend API
cd ../backend-api && npm start

# Python service
cd ../python-service && uvicorn app.main:app
```

### Issue: Port 3001 already in use

**Solution:** Change port in `vite.config.js`:
```javascript
server: { port: 3002 }
```

### Issue: Build fails

**Solution:** Clear cache and reinstall:
```bash
rm -rf node_modules dist
npm install
npm run build
```

## Contributing

1. Create feature branch
2. Make changes
3. Run tests: `npm test`
4. Run linter: `npm run lint:fix`
5. Build: `npm run build`
6. Submit pull request

## License

MIT License

## Support

For issues, open a GitHub issue.

---

**Project:** DevOps Master's Degree Research
**Version:** 1.0.0
**Last Updated:** December 2025
 
 