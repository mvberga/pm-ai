import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');

// Test configuration
export const options = {
  stages: [
    { duration: '2m', target: 10 }, // Ramp up to 10 users over 2 minutes
    { duration: '5m', target: 10 }, // Stay at 10 users for 5 minutes
    { duration: '2m', target: 0 },  // Ramp down to 0 users over 2 minutes
  ],
  thresholds: {
    http_req_duration: ['p(95)<2000'], // 95% of requests must complete below 2s
    http_req_failed: ['rate<0.1'],     // Error rate must be below 10%
    errors: ['rate<0.1'],              // Custom error rate must be below 10%
  },
};

// Base URL
const BASE_URL = 'http://localhost:8000';

// Test data
const testUser = {
  email: 'test@example.com',
  password: 'testpassword123'
};

export function setup() {
  // Setup: Create test user and get auth token
  const registerResponse = http.post(`${BASE_URL}/api/v1/auth/register`, JSON.stringify(testUser), {
    headers: { 'Content-Type': 'application/json' },
  });
  
  if (registerResponse.status === 201 || registerResponse.status === 400) {
    // User already exists or was created
    const loginResponse = http.post(`${BASE_URL}/api/v1/auth/login`, JSON.stringify(testUser), {
      headers: { 'Content-Type': 'application/json' },
    });
    
    if (loginResponse.status === 200) {
      const token = JSON.parse(loginResponse.body).access_token;
      return { token };
    }
  }
  
  return { token: null };
}

export default function(data) {
  const headers = {
    'Content-Type': 'application/json',
  };
  
  if (data.token) {
    headers['Authorization'] = `Bearer ${data.token}`;
  }

  // Test 1: Health check
  const healthResponse = http.get(`${BASE_URL}/health`);
  check(healthResponse, {
    'health check status is 200': (r) => r.status === 200,
    'health check response time < 500ms': (r) => r.timings.duration < 500,
  }) || errorRate.add(1);

  sleep(1);

  // Test 2: API root
  const apiResponse = http.get(`${BASE_URL}/api/v1/`);
  check(apiResponse, {
    'API root status is 200': (r) => r.status === 200,
    'API root response time < 1000ms': (r) => r.timings.duration < 1000,
  }) || errorRate.add(1);

  sleep(1);

  // Test 3: Get projects (if authenticated)
  if (data.token) {
    const projectsResponse = http.get(`${BASE_URL}/api/v1/projects/`, { headers });
    check(projectsResponse, {
      'projects status is 200': (r) => r.status === 200,
      'projects response time < 1500ms': (r) => r.timings.duration < 1500,
    }) || errorRate.add(1);

    sleep(1);

    // Test 4: Create a project
    const newProject = {
      name: `Load Test Project ${__VU}_${__ITER}`,
      description: 'Project created during load testing',
      status: 'active'
    };
    
    const createResponse = http.post(`${BASE_URL}/api/v1/projects/`, JSON.stringify(newProject), { headers });
    check(createResponse, {
      'create project status is 201': (r) => r.status === 201,
      'create project response time < 2000ms': (r) => r.timings.duration < 2000,
    }) || errorRate.add(1);

    sleep(1);

    // Test 5: Get project details (if project was created)
    if (createResponse.status === 201) {
      const projectId = JSON.parse(createResponse.body).id;
      const projectResponse = http.get(`${BASE_URL}/api/v1/projects/${projectId}`, { headers });
      check(projectResponse, {
        'project details status is 200': (r) => r.status === 200,
        'project details response time < 1000ms': (r) => r.timings.duration < 1000,
      }) || errorRate.add(1);
    }
  }

  sleep(1);

  // Test 6: Get portfolios (if authenticated)
  if (data.token) {
    const portfoliosResponse = http.get(`${BASE_URL}/api/v1/portfolios/`, { headers });
    check(portfoliosResponse, {
      'portfolios status is 200': (r) => r.status === 200,
      'portfolios response time < 1500ms': (r) => r.timings.duration < 1500,
    }) || errorRate.add(1);
  }

  sleep(1);
}

export function teardown(data) {
  // Cleanup: Remove test data if needed
  console.log('Load test completed');
}
