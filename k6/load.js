import http from 'k6/http';
import { check, sleep } from 'k6';
import { uuidv4, randomIntBetween } from 'https://jslib.k6.io/k6-utils/1.4.0/index.js';

export let options = {
  vus: 100,
  duration: '300s',
};

const BASE_URL = 'http://localhost:8080';

export default function () {
  const userPayload = JSON.stringify({
    name: 'John Doe',
    email: `user_${__VU}_${__ITER}@example.com`,
    timezone: 'UTC',
    birthday: new Date().toISOString()
  });

  const userRes = http.post(`${BASE_URL}/users`, userPayload, {
    headers: { 'Content-Type': 'application/json' }
  });

  check(userRes, {
    'user created (200)': (r) => r.status === 200
  });

  const userId = userRes.json().data.id;

  const getUserRes = http.get(`${BASE_URL}/users/${userId}`);
  check(getUserRes, {
    'user fetched (200)': (r) => r.status === 200
  });

  const updatePayload = JSON.stringify({
    name: 'Jane Doe',
    email: `updated_${__VU}_${__ITER}@example.com`,
    timezone: 'UTC+3',
    birthday: new Date().toISOString()
  });

  const updateUserRes = http.put(`${BASE_URL}/users/${userId}`, updatePayload, {
    headers: { 'Content-Type': 'application/json' }
  });

  check(updateUserRes, {
    'user updated (200)': (r) => r.status === 200
  });

  const numMeasurements = randomIntBetween(1000, 5000);
  const now = new Date();

  for (let i = 0; i < numMeasurements; i++) {
    const measurementDate = new Date(now);
    measurementDate.setDate(now.getDate() + i);

    const measurementPayload = JSON.stringify({
      systolic: 100 + (i % 40),
      diastolic: 60 + (i % 20),
      pulse: 60 + (i % 30),
      drug: 'None',
      note: `Measurement #${i + 1}`,
      date: measurementDate.toISOString()
    });

    const measurementRes = http.post(`${BASE_URL}/measurements`, measurementPayload, {
      headers: {
        'Content-Type': 'application/json',
        'user-id': userId
      }
    });

    check(measurementRes, {
      [`measurement ${i + 1} created (200)`]: (r) => r.status === 200
    });

    sleep(0.005);
  }

  const getAllRes = http.get(`${BASE_URL}/measurements`, {
    headers: { 'user-id': userId }
  });

  check(getAllRes, {
    'measurements fetched (200)': (r) => r.status === 200
  });

  const reportRes = http.post(`${BASE_URL}/reports/generate`, null, {
    headers: { 'user-id': userId }
  });

  check(reportRes, {
    'report requested (200)': (r) => r.status === 200
  });

  sleep(1);
}
