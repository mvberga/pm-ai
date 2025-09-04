import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');

// Test configuration - Spike test with sudden load increases
export const options = {
  stages: [
    { duration: '1m', target: 10 },   // Normal load: 10 users
    { duration: '30s', target: 100 }, // Spike: 100 users (10x increase)
    { duration: '1m', target: 10 },   // Back to normal: 10 users
    { duration: '30s', target: 150 }, // Another spike: 150 users
    { duration: '1m', target: 10 },   // Back to normal: 10 users
    { duration: '30s', target: 0 },   // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<10000'], // 95% of requests must complete below 10s
    http_req_failed: ['rate<0.3'],      // Error rate must be below 30%
    errors: ['rate<0.3'],               // Custom error rate must be below 30%
  },
};

// Base URL
const BASE_URL = 'http://localhost:8000';

// Test data
const testUser = {
  email: 'spike@example.com',
  password: 'spikepassword123'
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

  // Spike test scenarios - test system recovery from sudden load

  // Scenario 1: Health check (should always work)
  const healthResponse = http.get(`${BASE_URL}/health`);
  check(healthResponse, {
    'health check status is 200': (r) => r.status === 200,
    'health check response time < 2000ms': (r) => r.timings.duration < 2000,
  }) || errorRate.add(1);

  // Scenario 2: API root
  const apiResponse = http.get(`${BASE_URL}/api/v1/`);
  check(apiResponse, {
    'API root status is 200': (r) => r.status === 200,
  }) || errorRate.add(1);

  // Scenario 3: Authenticated operations (more resource intensive)
  if (data.token) {
    // Get projects
    const projectsResponse = http.get(`${BASE_URL}/api/v1/projects/`, { headers });
    check(projectsResponse, {
      'projects status is 200': (r) => r.status === 200,
    }) || errorRate.add(1);

    // Create project (database intensive)
    const newProject = {
      name: `Spike Test Project ${__VU}_${__ITER}_${Date.now()}`,
      description: 'Project created during spike testing',
      status: 'active'
    };
    
    const createResponse = http.post(`${BASE_URL}/api/v1/projects/`, JSON.stringify(newProject), { headers });
    check(createResponse, {
      'create project status is 201': (r) => r.status === 201,
    }) || errorRate.add(1);

    // Get portfolios
    const portfoliosResponse = http.get(`${BASE_URL}/api/v1/portfolios/`, { headers });
    check(portfoliosResponse, {
      'portfolios status is 200': (r) => r.status === 200,
    }) || errorRate.add(1);
  }

  // Scenario 4: Authentication operations (CPU intensive)
  const authTestUser = {
    email: `spike_auth_${__VU}_${__ITER}_${Date.now()}@example.com`,
    password: 'spikepassword123'
  };
  
  const authResponse = http.post(`${BASE_URL}/api/v1/auth/register`, JSON.stringify(authTestUser), {
    headers: { 'Content-Type': 'application/json' },
  });
  
  check(authResponse, {
    'auth registration status is 201 or 400': (r) => r.status === 201 || r.status === 400,
  }) || errorRate.add(1);

  // Scenario 5: Concurrent read operations
  if (data.token) {
    // Multiple concurrent reads
    const readPromises = [];
    for (let i = 0; i < 3; i++) {
      readPromises.push(http.get(`${BASE_URL}/api/v1/projects/`, { headers }));
    }
    
    const readResponses = readPromises;
    readResponses.forEach((response, index) => {
      check(response, {
        [`concurrent read ${index} status is 200`]: (r) => r.status === 200,
      }) || errorRate.add(1);
    });
  }

  // Minimal sleep to maximize load during spikes
  sleep(0.1);
}

export function teardown(data) {
  console.log('Spike test completed');
}
