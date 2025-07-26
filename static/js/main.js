// main.js (or specific script for a page)

const API_BASE_URL = 'http://127.0.0.1:5000'; // Your Flask backend URL

async function fetchData(endpoint, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
    };
    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        const result = await response.json(); // Always try to parse JSON
        if (!response.ok) {
            // If response.status is not 2xx, it's an error
            const error = new Error(result.message || 'Something went wrong');
            error.status = response.status;
            throw error;
        }
        return result; // Return the parsed JSON data
    } catch (error) {
        console.error('API call failed:', error);
        throw error; // Re-throw to be handled by the calling function
    }
}