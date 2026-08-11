# API Documentation

**Version:** 0.1.0

This document describes the available endpoints for the FastAPI-based service, including request/response formats and validation error handling.

---

## Table of Contents

- [Endpoints](#endpoints)
  - [POST /upload](#post-upload)
  - [POST /query](#post-query)
  - [POST /feedback](#post-feedback)
- [Schemas](#schemas)
- [Error Handling](#error-handling)

---

## Endpoints

### POST /upload

**Summary:** Upload File

Uploads a file along with a department identifier. Used to ingest documents into the system (e.g., for retrieval-augmented generation).

**Request Content-Type:** `multipart/form-data`

**Request Body Fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `file` | binary (`application/octet-stream`) | Yes | The file to upload |
| `department` | string | Yes | Department the file belongs to |

**Example Request (cURL):**

```bash
curl -X POST "https://<host>/upload" \
  -F "file=@document.pdf" \
  -F "department=Finance"
```

**Responses:**

| Status | Description |
|---|---|
| `200` | Successful upload. Returns a JSON response (schema not strictly typed). |
| `422` | Validation error. Returns a `HTTPValidationError` object. |

---

### POST /query

**Summary:** Chat Query

Submits a question to the chat/retrieval system and returns a generated answer with supporting citations and retrieved context chunks.

**Request Content-Type:** `application/json`

**Request Body:** [`ChatRequest`](#chatrequest)

| Field | Type | Required | Description |
|---|---|---|---|
| `question` | string | Yes | The user's question |
| `session_id` | string | Yes | Identifier for the chat session |

**Example Request:**

```json
{
  "question": "What is the reimbursement policy for travel expenses?",
  "session_id": "session-12345"
}
```

**Response Body:** [`ChatResponse`](#chatresponse)

| Field | Type | Required | Description |
|---|---|---|---|
| `answer` | string | Yes | The generated answer |
| `citations` | array | Yes | List of citation objects supporting the answer |
| `retrieved_chunks` | array | Yes | List of retrieved context chunks used to generate the answer |
| `agent_used` | string \| null | No | Name of the agent that handled the query, if applicable |

**Example Response:**

```json
{
  "answer": "Travel expenses are reimbursed within 30 days of submission...",
  "citations": [],
  "retrieved_chunks": [],
  "agent_used": "finance_agent"
}
```

**Responses:**

| Status | Description |
|---|---|
| `200` | Successful response. Returns a `ChatResponse` object. |
| `422` | Validation error. Returns a `HTTPValidationError` object. |

---

### POST /feedback

**Summary:** Submit Feedback

Submits user feedback on a previous chat response, including the original question, retrieved chunks, final answer, and feedback text.

**Request Content-Type:** `application/json`

**Request Body:** [`FeedbackRequest`](#feedbackrequest)

| Field | Type | Required | Description |
|---|---|---|---|
| `session_id` | string | Yes | Identifier for the chat session |
| `question` | string | Yes | The original question asked |
| `retrieved_chunks` | array of strings | Yes | Chunks that were retrieved for this query |
| `final_answer` | string | Yes | The final answer that was returned |
| `feedback` | string | Yes | User-provided feedback text |
| `timestamp` | string | Yes | Timestamp of the feedback submission |

**Example Request:**

```json
{
  "session_id": "session-12345",
  "question": "What is the reimbursement policy for travel expenses?",
  "retrieved_chunks": ["chunk_1", "chunk_2"],
  "final_answer": "Travel expenses are reimbursed within 30 days of submission...",
  "feedback": "This answer was helpful and accurate.",
  "timestamp": "2026-08-12T10:15:00Z"
}
```

**Responses:**

| Status | Description |
|---|---|
| `200` | Successful submission. Returns a JSON response (schema not strictly typed). |
| `422` | Validation error. Returns a `HTTPValidationError` object. |

---

## Schemas

### ChatRequest

| Field | Type | Required |
|---|---|---|
| `question` | string | Yes |
| `session_id` | string | Yes |

### ChatResponse

| Field | Type | Required |
|---|---|---|
| `answer` | string | Yes |
| `citations` | array | Yes |
| `retrieved_chunks` | array | Yes |
| `agent_used` | string \| null | No |

### FeedbackRequest

| Field | Type | Required |
|---|---|---|
| `session_id` | string | Yes |
| `question` | string | Yes |
| `retrieved_chunks` | array of strings | Yes |
| `final_answer` | string | Yes |
| `feedback` | string | Yes |
| `timestamp` | string | Yes |

### Body_upload_file_upload_post

| Field | Type | Required |
|---|---|---|
| `file` | binary | Yes |
| `department` | string | Yes |

---

## Error Handling

All endpoints may return a `422 Unprocessable Entity` response when request validation fails. The error body follows the `HTTPValidationError` schema:

```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "field required",
      "type": "value_error.missing",
      "input": null,
      "ctx": {}
    }
  ]
}
```

### ValidationError Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `loc` | array (string or integer) | Yes | Location of the error (e.g., body field path) |
| `msg` | string | Yes | Human-readable error message |
| `type` | string | Yes | Error type identifier |
| `input` | any | No | The invalid input value that was provided |
| `ctx` | object | No | Additional context about the error |
