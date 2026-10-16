# Descriptive Statistics & CORS-Aware FastAPI Service

A lightweight, high-performance **FastAPI service** that computes descriptive statistics for dynamic integer datasets while enforcing a strict per-origin Cross-Origin Resource Sharing (CORS) policy. The service also includes custom middleware for unique request tracking and precise request processing-time measurement.

**Live Deployment:** https://cors-aware-metrics-api-xor2.onrender.com

![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-REST%20API-009688.svg?style=flat&logo=fastapi&logoColor=white)
![CORS](https://img.shields.io/badge/CORS-Origin%20Restricted-blue.svg?style=flat)
![Deployment](https://img.shields.io/badge/Deployed%20on-Render-46E3B7.svg?style=flat&logo=render&logoColor=white)

---

## ✨ Features

- **Dynamic Descriptive Statistics:** Calculates `count`, `sum`, `min`, `max`, and `mean` for comma-separated integer sequences.
- **Strict CORS Policy:** Allows cross-origin browser requests exclusively from the configured origin, `https://dash-l6xt5u.example.com`.
- **Request Tracking:** Generates a unique UUID v4 for each incoming request through the `X-Request-ID` header.
- **Processing-Time Measurement:** Reports request processing duration through the `X-Process-Time` response header.
- **Input Validation:** Rejects missing, empty, or invalid numeric input with an appropriate HTTP error response.
- **Custom Middleware:** Adds tracking headers to responses, including standard HTTP errors and CORS preflight responses, when correctly configured.
- **Interactive API Documentation:** Supports endpoint exploration through FastAPI's Swagger UI.

## 🚀 Live API

The deployed application is available at:

```text
https://cors-aware-metrics-api-xor2.onrender.com
```

| Endpoint | Method | Purpose |
|---|---|---|
| `/stats` | GET | Computes descriptive statistics |
| `/docs` | GET | Opens interactive Swagger documentation |
| `/openapi.json` | GET | Returns the OpenAPI specification |

## 📌 API Reference

### `GET /stats`

Computes summary statistics for a comma-separated sequence of integers.

#### Query Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `values` | String | Yes | Comma-separated integers, such as `10,20,30,40,50` |

#### Example Request

```bash
curl -i "https://cors-aware-metrics-api-xor2.onrender.com/stats?values=10,20,30,40,50"
```

#### Example Response — `200 OK`

```json
{
  "email": "your-email@example.com",
  "count": 5,
  "sum": 150,
  "min": 10,
  "max": 50,
  "mean": 30.0
}
```

The email shown is a placeholder. The actual response depends on the deployment's `EMAIL` configuration.

#### Response Field Descriptions

| Field | Type | Description |
|---|---|---|
| `email` | String | Identifier associated with the deployment |
| `count` | Integer | Number of integers processed |
| `sum` | Integer | Sum of all input integers |
| `min` | Integer | Minimum integer in the dataset |
| `max` | Integer | Maximum integer in the dataset |
| `mean` | Float | Arithmetic mean of the input integers |

The mean is calculated as:

\[
\text{Mean}=\frac{\text{Sum of all values}}{\text{Count}}
\]

For example, given `10,20,30,40,50`, the mean is `30.0`.

### Error Responses

Invalid input is expected to return an HTTP `400 Bad Request` response when the application explicitly validates these conditions.

| Condition | Example |
|---|---|
| Missing parameter | `/stats` |
| Empty input | `/stats?values=` |
| Non-numeric input | `/stats?values=10,abc,30` |
| Invalid integer sequence | `/stats?values=10,,30` |

Example error response:

```json
{
  "detail": "Invalid values parameter"
}
```

The exact error message depends on the implementation.

## 🌐 CORS Policy

The service restricts browser-based cross-origin access to a single permitted origin.

### Allowed Origin

```text
https://dash-l6xt5u.example.com
```

Requests from this origin can receive the following response header:

```http
Access-Control-Allow-Origin: https://dash-l6xt5u.example.com
```

### Disallowed Origins

Other origins, such as `https://unauthorized-domain.com`, should not receive an `Access-Control-Allow-Origin` header authorizing access.

The service does not use a wildcard (`*`) origin policy.

**Important:** CORS is a browser security mechanism. It does not prevent direct HTTP requests from command-line clients, scripts, or other servers. Use authentication and authorization separately if the API requires access control.

## ⚙️ Custom Middleware Headers

The application uses custom response headers for request tracing and performance measurement.

### `X-Request-ID`

A unique UUID v4 identifying an individual request.

Example:

```http
X-Request-ID: 8f3c7a92-4b21-4d10-b98a-2e38c9029e12
```

### `X-Process-Time`

The elapsed processing time measured by the middleware, expressed in seconds.

Example:

```http
X-Process-Time: 0.000452
```

The value above is illustrative; actual processing time varies by request and server load.

These headers are intended to be included on successful responses, errors, and CORS preflight responses when middleware is configured to cover all response paths.

## 🧪 Verification and Testing

Use the following commands to verify the deployed service.

### 1. Test an Allowed-Origin Preflight

```bash
curl -i -X OPTIONS \
  "https://cors-aware-metrics-api-xor2.onrender.com/stats" \
  -H "Origin: https://dash-l6xt5u.example.com" \
  -H "Access-Control-Request-Method: GET"
```

**Expected behavior:**

- The response permits the configured origin.
- The response includes `X-Request-ID`.
- The response includes `X-Process-Time`.

### 2. Test a Disallowed-Origin Preflight

```bash
curl -i -X OPTIONS \
  "https://cors-aware-metrics-api-xor2.onrender.com/stats" \
  -H "Origin: https://unauthorized-domain.com" \
  -H "Access-Control-Request-Method: GET"
```

**Expected behavior:**

- The response does not authorize the unapproved origin.
- No `Access-Control-Allow-Origin` header should grant access to that origin.
- Middleware tracking headers should be present if configured for all responses.

A preflight response may still return a successful HTTP status for a disallowed origin. The important behavior is that the response does not authorize that origin.

### 3. Test Statistics Calculation

```bash
curl -i \
  "https://cors-aware-metrics-api-xor2.onrender.com/stats?values=10,20,30,40,50"
```

**Expected response:**

```json
{
  "email": "your-email@example.com",
  "count": 5,
  "sum": 150,
  "min": 10,
  "max": 50,
  "mean": 30.0
}
```

### 4. Test Invalid Input

```bash
curl -i \
  "https://cors-aware-metrics-api-xor2.onrender.com/stats?values=10,abc,30"
```

**Expected behavior:** An HTTP `400 Bad Request` response with an error description, assuming the application implements the documented validation.

## 📁 Project Structure

```text
.
├── main.py           # FastAPI application, routes, and middleware
├── requirements.txt  # Project dependencies
└── README.md         # Project documentation
```

## 🛠️ Local Setup and Development

### Prerequisites

- Python 3.10 or later
- pip
- Git

### 1. Clone the Repository

Replace the placeholder URL with your actual GitHub repository URL.

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Create a Virtual Environment

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Ensure `requirements.txt` includes FastAPI and an ASGI server such as Uvicorn, along with any other dependencies used by your implementation.

### 4. Configure Environment Variables

The service supports an optional `EMAIL` environment variable.

**Linux / macOS**

```bash
export EMAIL="your-email@example.com"
```

**Windows PowerShell**

```powershell
$env:EMAIL = "your-email@example.com"
```

If the variable is not set, the documented default is `your-email@example.com`.

### 5. Run the Application

```bash
uvicorn main:app --reload --port 8000
```

The local service will be available at:

- API endpoint: http://localhost:8000/stats
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Test the local API:

```bash
curl -i "http://localhost:8000/stats?values=10,20,30,40,50"
```

## 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| CORS middleware | Cross-origin request policy |
| UUID | Unique request identifiers |
| Environment variables | Deployment-specific configuration |
| Render | Cloud hosting |

## 🔄 Request Processing Workflow

1. The client sends a request to the FastAPI service.
2. Middleware generates a unique request ID and measures processing time.
3. The CORS policy evaluates the request origin and handles preflight requests.
4. The `/stats` endpoint parses and validates the integer sequence.
5. The service computes the count, sum, minimum, maximum, and mean.
6. The API returns the JSON result with the configured middleware headers.

## 🔒 Production Considerations

- Keep the allowed-origin list explicit and avoid unrestricted wildcard policies.
- Validate query parameters and handle malformed numeric sequences consistently.
- Use authentication and authorization when endpoints expose protected information.
- Ensure middleware headers are added to error responses and preflight responses.
- Avoid exposing sensitive operational information in API responses.
- Add automated tests for valid input, invalid input, CORS behavior, and response headers.
- Monitor deployment health, latency, and error rates.

---

**Built with FastAPI for reliable statistics, controlled cross-origin access, and request-level observability.**
