const request = require('supertest');
const app = require('./server');

describe('Backend API Tests', () => {
  describe('GET /health', () => {
    it('should return health status', async () => {
      const res = await request(app).get('/health');

      expect(res.statusCode).toBe(200);
      expect(res.body).toHaveProperty('status', 'healthy');
      expect(res.body).toHaveProperty('timestamp');
      expect(res.body).toHaveProperty('uptime');
    });
  });

  describe('GET /api/v1/users', () => {
    it('should return list of users', async () => {
      const res = await request(app).get('/api/v1/users');

      expect(res.statusCode).toBe(200);
      expect(res.body).toHaveProperty('users');
      expect(Array.isArray(res.body.users)).toBe(true);
      expect(res.body.users.length).toBeGreaterThan(0);
    });
  });

  describe('GET /api/v1/users/:id', () => {
    it('should return user by ID', async () => {
      const res = await request(app).get('/api/v1/users/1');

      expect(res.statusCode).toBe(200);
      expect(res.body).toHaveProperty('id', 1);
      expect(res.body).toHaveProperty('name');
      expect(res.body).toHaveProperty('email');
    });

    it('should return 404 for non-existent user', async () => {
      const res = await request(app).get('/api/v1/users/999');

      expect(res.statusCode).toBe(404);
      expect(res.body).toHaveProperty('error');
    });
  });

  describe('POST /api/v1/users', () => {
    it('should create new user', async () => {
      const newUser = {
        name: 'Test User',
        email: 'test@example.com',
        role: 'user',
      };

      const res = await request(app)
        .post('/api/v1/users')
        .send(newUser);

      expect(res.statusCode).toBe(201);
      expect(res.body).toHaveProperty('id');
      expect(res.body).toHaveProperty('name', newUser.name);
      expect(res.body).toHaveProperty('email', newUser.email);
    });

    it('should return 400 if name is missing', async () => {
      const invalidUser = {
        email: 'test@example.com',
      };

      const res = await request(app)
        .post('/api/v1/users')
        .send(invalidUser);

      expect(res.statusCode).toBe(400);
      expect(res.body).toHaveProperty('error');
    });
  });

  describe('GET /metrics', () => {
    it('should return Prometheus metrics', async () => {
      const res = await request(app).get('/metrics');

      expect(res.statusCode).toBe(200);
      expect(res.text).toContain('http_requests_total');
      expect(res.headers['content-type']).toContain('text/plain');
    });
  });

  describe('404 handling', () => {
    it('should return 404 for unknown routes', async () => {
      const res = await request(app).get('/unknown-route');

      expect(res.statusCode).toBe(404);
      expect(res.body).toHaveProperty('error', 'Not found');
    });
  });
});
