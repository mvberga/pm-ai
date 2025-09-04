import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');

// Test configuration
export const options = {
  stages: [
    { duration: '2m', target: 20 },  // Ramp up to 20 users
    { duration: '5m', target: 20 },  // Stay at 20 users
    { duration: '2m', target: 50 },  // Ramp up to 50 users (stress)
    { duration: '5m', target: 50 },  // Stay at 50 users
    { duration: '2m', target: 0 },   // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<5000'], // 95% of requests must complete below 5s
    http_req_failed: ['rate<0.2'],     // Error rate must be below 20%
    errors: ['rate<0.2'],              // Custom error rate must be below 20%
  },
};

// Base URL
const BASE_URL = 'http://localhost:8000';

// Test data
const testUser = {
  email: 'stress@example.com',
  password: 'stresspassword123'
};

export function setup() {
  // Setup: Create test user and get auth token
  const registerResponse = http.post(`${BASE_URL}/api/v1/auth/register`, JSON.stringify(testUser), {
    headers: { 'Content-Type': 'application/json' },
  });
  
  if (registerResponse.status === 201 || registerResponse.status === 400) {
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

  // Stress test scenarios

  // Scenario 1: Rapid API calls
  const healthResponse = http.get(`${BASE_URL}/health`);
  check(healthResponse, {
    'health check status is 200': (r) => r.status === 200,
  }) || errorRate.add(1);

  // Scenario 2: Concurrent project operations
  if (data.token) {
    // Get projects
    const projectsResponse = http.get(`${BASE_URL}/api/v1/projects/`, { headers });
    check(projectsResponse, {
      'projects status is 200': (r) => r.status === 200,
    }) || errorRate.add(1);

    // Create project
    const newProject = {
      name: `Stress Test Project ${__VU}_${__ITER}_${Date.now()}`,
      description: 'Project created during stress testing',
      status: 'active'
    };
    
    const createResponse = http.post(`${BASE_URL}/api/v1/projects/`, JSON.stringify(newProject), { headers });
    check(createResponse, {
      'create project status is 201': (r) => r.status === 201,
    }) || errorRate.add(1);

    // Update project (if created)
    if (createResponse.status === 201) {
      const projectId = JSON.parse(createResponse.body).id;
      const updateData = {
        name: `Updated Stress Test Project ${__VU}_${__ITER}`,
        description: 'Updated during stress testing'
      };
      
      const updateResponse = http.put(`${BASE_URL}/api/v1/projects/${projectId}`, JSON.stringify(updateData), { headers });
      check(updateResponse, {
        'update project status is 200': (r) => r.status === 200,
      }) || errorRate.add(1);
    }
  }

  // Scenario 3: Portfolio operations
  if (data.token) {
    const portfoliosResponse = http.get(`${BASE_URL}/api/v1/portfolios/`, { headers });
    check(portfoliosResponse, {
      'portfolios status is 200': (r) => r.status === 200,
    }) || errorRate.add(1);
  }

  // Scenario 4: Authentication stress
  const authTestUser = {
    email: `stress_auth_${__VU}_${__ITER}@example.com`,
    password: 'stresspassword123'
  };
  
  const authResponse = http.post(`${BASE_URL}/api/v1/auth/register`, JSON.stringify(authTestUser), {
    headers: { 'Content-Type': 'application/json' },
  });
  
  check(authResponse, {
    'auth registration status is 201 or 400': (r) => r.status === 201 || r.status === 400,
  }) || errorRate.add(1);

  // Short sleep to prevent overwhelming the system
  sleep(0.5);
}

export function teardown(data) {
  console.log('Stress test completed');
}
