import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');

// Test configuration - Volume test with large amounts of data
export const options = {
  stages: [
    { duration: '2m', target: 5 },    // Start with 5 users
    { duration: '10m', target: 5 },   // Stay at 5 users for 10 minutes (volume test)
    { duration: '2m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<3000'], // 95% of requests must complete below 3s
    http_req_failed: ['rate<0.1'],     // Error rate must be below 10%
    errors: ['rate<0.1'],              // Custom error rate must be below 10%
  },
};

// Base URL
const BASE_URL = 'http://localhost:8000';

// Test data
const testUser = {
  email: 'volume@example.com',
  password: 'volumepassword123'
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

  // Volume test scenarios - test system with large amounts of data

  // Scenario 1: Create multiple projects (volume of data)
  if (data.token) {
    for (let i = 0; i < 5; i++) {
      const newProject = {
        name: `Volume Test Project ${__VU}_${__ITER}_${i}_${Date.now()}`,
        description: `This is a volume test project with a longer description to test how the system handles larger amounts of data. Project ${i} created during volume testing. This description contains more text to simulate real-world data volume.`,
        status: 'active',
        metadata: {
          created_by: 'volume_test',
          test_iteration: __ITER,
          virtual_user: __VU,
          timestamp: Date.now(),
          additional_data: 'x'.repeat(100) // Add some extra data
        }
      };
      
      const createResponse = http.post(`${BASE_URL}/api/v1/projects/`, JSON.stringify(newProject), { headers });
      check(createResponse, {
        [`create project ${i} status is 201`]: (r) => r.status === 201,
        [`create project ${i} response time < 2000ms`]: (r) => r.timings.duration < 2000,
      }) || errorRate.add(1);
    }
  }

  // Scenario 2: Bulk read operations
  if (data.token) {
    // Get all projects multiple times
    for (let i = 0; i < 3; i++) {
      const projectsResponse = http.get(`${BASE_URL}/api/v1/projects/`, { headers });
      check(projectsResponse, {
        [`bulk read ${i} status is 200`]: (r) => r.status === 200,
        [`bulk read ${i} response time < 1500ms`]: (r) => r.timings.duration < 1500,
      }) || errorRate.add(1);
    }

    // Get all portfolios multiple times
    for (let i = 0; i < 3; i++) {
      const portfoliosResponse = http.get(`${BASE_URL}/api/v1/portfolios/`, { headers });
      check(portfoliosResponse, {
        [`bulk portfolios read ${i} status is 200`]: (r) => r.status === 200,
        [`bulk portfolios read ${i} response time < 1500ms`]: (r) => r.timings.duration < 1500,
      }) || errorRate.add(1);
    }
  }

  // Scenario 3: Large data operations
  if (data.token) {
    // Create a project with large description
    const largeProject = {
      name: `Large Volume Project ${__VU}_${__ITER}_${Date.now()}`,
      description: 'x'.repeat(1000), // Large description
      status: 'active',
      metadata: {
        large_data: 'x'.repeat(5000), // Large metadata
        test_type: 'volume',
        iteration: __ITER,
        user: __VU
      }
    };
    
    const largeCreateResponse = http.post(`${BASE_URL}/api/v1/projects/`, JSON.stringify(largeProject), { headers });
    check(largeCreateResponse, {
      'large project creation status is 201': (r) => r.status === 201,
      'large project creation response time < 3000ms': (r) => r.timings.duration < 3000,
    }) || errorRate.add(1);
  }

  // Scenario 4: Authentication with volume
  const authTestUser = {
    email: `volume_auth_${__VU}_${__ITER}_${Date.now()}@example.com`,
    password: 'volumepassword123'
  };
  
  const authResponse = http.post(`${BASE_URL}/api/v1/auth/register`, JSON.stringify(authTestUser), {
    headers: { 'Content-Type': 'application/json' },
  });
  
  check(authResponse, {
    'volume auth registration status is 201 or 400': (r) => r.status === 201 || r.status === 400,
    'volume auth response time < 1000ms': (r) => r.timings.duration < 1000,
  }) || errorRate.add(1);

  // Scenario 5: Health checks with volume
  for (let i = 0; i < 2; i++) {
    const healthResponse = http.get(`${BASE_URL}/health`);
    check(healthResponse, {
      [`volume health check ${i} status is 200`]: (r) => r.status === 200,
      [`volume health check ${i} response time < 500ms`]: (r) => r.timings.duration < 500,
    }) || errorRate.add(1);
  }

  // Scenario 6: API root with volume
  for (let i = 0; i < 2; i++) {
    const apiResponse = http.get(`${BASE_URL}/api/v1/`);
    check(apiResponse, {
      [`volume API root ${i} status is 200`]: (r) => r.status === 200,
      [`volume API root ${i} response time < 1000ms`]: (r) => r.timings.duration < 1000,
    }) || errorRate.add(1);
  }

  // Longer sleep for volume test to simulate real usage patterns
  sleep(2);
}

export function teardown(data) {
  console.log('Volume test completed');
}
