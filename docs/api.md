# Lexiai Server API

## Introduction

The Lexiai Server API is a RESTful API that allows you to interact with the Lexiai Server. The API is designed to be simple and easy to use, and is based on the HTTP protocol.

## Authentication

### Register

Registers a new user account.

**Endpoint**: `POST /api/users/register`

**Request Headers**:
- Content-Type: application/json

**Request Body**:
```json
{
    "username": "username",
    "email": "test@mail.com",
    "password": "password"
}
```

**Field Descriptions**:
- `username`: Required. Length: 3-20 characters. Alphanumeric characters only.
- `email`: Required. Must be a valid email address format.
- `password`: Required. Minimum 6 characters, must contain at least one uppercase letter, one lowercase letter, one number and one special character.

**Success Response**:
- Status Code: 200 OK
```json
{
    "message": "User registered successfully"
}
```

**Error Response**:
- Status Code: 400 Bad Request
```json
{
    "message": "Email already exists."
}
```

### Login

Authenticates a user and returns an access token.

**Endpoint**: `POST /api/users/login`

**Request Headers**:
- Content-Type: application/json

**Request Body**:
```json
{
    "email": "test@mail.com",
    "password": "Aa123#"
}
```

**Field Descriptions**:
- `email`: Required. The registered email address.
- `password`: Required. The user's password.

**Success Response**:
- Status Code: 200 OK
```json
{
    "message": "Login successful",
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
        "_id": "67937e428f1a3daf58ec0cea",
        "username": "test",
        "email": "test@mail.com",
        "createdAt": "2025-01-24T11:49:22.734000",
        "settings": {
            "favorites": {
                "678559ac79bc79eeab784fe9": true
            },
            "language_id": "67867c4768c21d7deb4a8200",
            "style_id": "6785601479bc79eeab784ffd"
        }
    }
}
```

**Response Fields**:
- `message`: Success message
- `accessToken`: JWT token for authenticating subsequent requests
- `user`: Object containing user information
  - `_id`: Unique user identifier
  - `username`: User's username
  - `email`: User's email address
  - `createdAt`: Account creation timestamp
  - `settings`: User preferences and settings
    - `favorites`: Map of favorite items
    - `language_id`: Preferred language identifier
    - `style_id`: Preferred style identifier

**Error Response**:
- Status Code: 400 Bad Request
```json
{
    "message": "Invalid credentials"
}
```

## Styles

### Get All Styles

Retrieves a list of all available AI communication styles.

**Endpoint**: `GET /api/styles`

**Request Headers**: None required

**Success Response**:
- Status Code: 200 OK
```json
[
  {
    "_id": {
      "$oid": "6785601479bc79eeab784ffd"
    },
    "name": "Professional",
    "description": "Maintain a formal tone, be precise and thorough in your explanations. Focus on accuracy and clarity in all interactions."
  },
  {
    "_id": {
      "$oid": "6785601479bc79eeab784ffe"
    },
    "name": "Casual",
    "description": "Use a casual, approachable tone and be encouraging. Feel free to express enthusiasm when helping users."
  }
]
```

**Response Fields**:
- Array of Style objects:
  - `_id`: Object containing the style's unique identifier
    - `$oid`: MongoDB ObjectId string
  - `name`: Name of the communication style
  - `description`: Detailed description of the style characteristics

**Error Response**:
- Status Code: 500 Internal Server Error
```json
{
    "message": "Internal server error"
}
```

### Get Style by ID

Retrieves a specific AI communication style by its ID.

**Endpoint**: `GET /api/styles/{style_id}`

**Path Parameters**:
- `style_id`: The unique identifier of the style

**Request Headers**: None required

**Success Response**:
- Status Code: 200 OK
```json
{
  "_id": {
    "$oid": "6785601479bc79eeab784ffe"
  },
  "name": "Casual",
  "description": "Use a casual, approachable tone and be encouraging. Feel free to express enthusiasm when helping users."
}
```

**Response Fields**:
- `_id`: Object containing the style's unique identifier
  - `$oid`: MongoDB ObjectId string
- `name`: Name of the communication style
- `description`: Detailed description of the style characteristics

**Error Response**:
- Status Code: 404 Not Found
```json
{
    "message": "Style not found"
}
```

## Languages

### Get All Languages

Retrieves a list of all available languages.

**Endpoint**: `GET /api/languages`

**Request Headers**: None required

**Success Response**:
- Status Code: 200 OK
```json
[
  {
    "_id": {
      "$oid": "678557da79bc79eeab784fe4"
    },
    "name": "French"
  },
  {
    "_id": {
      "$oid": "6785965186ea7bd211eb2f9f"
    },
    "name": "Spanish"
  }
]
```

**Response Fields**:
- Array of Language objects:
  - `_id`: Object containing the language's unique identifier
    - `$oid`: MongoDB ObjectId string
  - `name`: Name of the language

**Error Response**:
- Status Code: 500 Internal Server Error
```json
{
    "message": "Internal server error"
}
```

### Get Language by ID

Retrieves a specific language by its ID.

**Endpoint**: `GET /api/languages/{language_id}`

**Path Parameters**:
- `language_id`: The unique identifier of the language

**Request Headers**: None required

**Success Response**:
- Status Code: 200 OK
```json
{
  "_id": {
    "$oid": "6785965186ea7bd211eb2f9f"
  },
  "name": "Spanish"
}
```

**Response Fields**:
- `_id`: Object containing the language's unique identifier
  - `$oid`: MongoDB ObjectId string
- `name`: Name of the language

**Error Response**:
- Status Code: 404 Not Found
```json
{
    "message": "Language not found"
}
```

## Topics

### Get Topics

Retrieves a list of available learning topics, with optional level filtering.

**Endpoint**: `GET /api/topics`

**Request Headers**:
- Authorization: Bearer {accessToken}
- Content-Type: application/json

**Query Parameters**:
- `level` (optional): Filter topics by difficulty level (e.g., "Beginner")
- `user_id` (optional): Filter topics by creator's unique identifier. If user_id equals `me`, Filter topics by the authenticated user's unique identifier.

**Success Response**:
- Status Code: 200 OK
```json
[
  {
    "_id": {
      "$oid": "678559ac79bc79eeab784fe9"
    },
    "title": "Introductions",
    "description": "Common introductions.",
    "level": "Beginner",
    "systemPrompt": "You are a friendly teacher helping a beginner learn common greetings...",
    "start": "Hello! Let's start with greetings",
    "createdAt": "2025-01-01T10:00:00Z",
    "user_id": {
      "$oid": "678ea72a7baff5011c1a27cf"
    },
    "user_info": {
      "username": "Danny",
      "email": "hd@hdcola.org"
    }
  }
]
```

**Response Fields**:
- Array of Topic objects:
  - `_id`: Object containing the topic's unique identifier
    - `$oid`: MongoDB ObjectId string
  - `title`: Title of the learning topic
  - `description`: Brief description of the topic
  - `level`: Difficulty level of the topic
  - `systemPrompt`: AI system prompt for the topic
  - `start`: Initial message to start the conversation
  - `createdAt`: Topic creation timestamp
  - `user_id`: Creator's unique identifier
    - `$oid`: MongoDB ObjectId string
  - `user_info`: Information about the topic creator
    - `username`: Creator's username
    - `email`: Creator's email

**Error Response**:
- Status Code: 401 Unauthorized
```json
{
    "message": "Authentication required"
}
```

### Create Topic

Creates a new learning topic.

**Endpoint**: `POST /api/topics`

**Request Headers**:
- Authorization: Bearer {accessToken}
- Content-Type: application/json

**Request Body**:
```json
{
  "title": "Bank",
  "description": "Go to the bank to handle business",
  "level": "Beginner",
  "systemPrompt": "Go to the bank to handle business",
  "start": "Hello! How can I help you today?"
}
```

**Field Descriptions**:
- `title`: Required. The title of the topic
- `description`: Required. Brief description of what will be learned
- `level`: Required. Difficulty level of the topic (e.g., "Beginner")
- `systemPrompt`: Required. Instructions for the AI system about how to conduct the lesson
- `start`: Required. The initial message to start the conversation

**Success Response**:
- Status Code: 201 Created
```json
{
  "_id": {
    "$oid": "678559ac79bc79eeab784fe9"
  },
  "title": "Bank",
  "description": "Go to the bank to handle business",
  "level": "Beginner",
  "systemPrompt": "Go to the bank to handle business",
  "start": "Hello! How can I help you today?",
  "createdAt": "2025-01-27T19:30:00Z",
  "user_id": {
    "$oid": "678ea72a7baff5011c1a27cf"
  }
}
```

**Error Response**:
- Status Code: 401 Unauthorized
```json
{
    "message": "Authentication required"
}
```
- Status Code: 400 Bad Request
```json
{
    "message": "Invalid topic data"
}
```

### Get Topic by ID

Retrieves a specific learning topic by its ID.

**Endpoint**: `GET /api/topics/{topic_id}`

**Path Parameters**:
- `topic_id`: The unique identifier of the topic

**Request Headers**:
- Authorization: Bearer {accessToken}
- Content-Type: application/json

**Success Response**:
- Status Code: 200 OK
```json
{
  "_id": {
    "$oid": "678559ac79bc79eeab784fe9"
  },
  "title": "Introductions",
  "description": "Common introductions.",
  "level": "Beginner",
  "systemPrompt": "You are a friendly teacher helping a beginner learn common greetings...",
  "start": "Hello! Let's start with greetings",
  "createdAt": "2025-01-01T10:00:00Z",
  "user_id": {
    "$oid": "678ea72a7baff5011c1a27cf"
  },
  "user_info": {
    "username": "Danny",
    "email": "hd@hdcola.org"
  }
}
```

**Response Fields**:
- `_id`: Object containing the topic's unique identifier
  - `$oid`: MongoDB ObjectId string
- `title`: Title of the learning topic
- `description`: Brief description of the topic
- `level`: Difficulty level of the topic
- `systemPrompt`: AI system prompt for the topic
- `start`: Initial message to start the conversation
- `createdAt`: Topic creation timestamp
- `user_id`: Creator's unique identifier
  - `$oid`: MongoDB ObjectId string
- `user_info`: Information about the topic creator
  - `username`: Creator's username
  - `email`: Creator's email

**Error Response**:
- Status Code: 404 Not Found
```json
{
    "message": "Topic not found"
}
```
- Status Code: 401 Unauthorized
```json
{
    "message": "Authentication required"
}
```

### Update Topic

Updates an existing learning topic.

**Endpoint**: `PUT /api/topics/{topic_id}`

**Path Parameters**:
- `topic_id`: The unique identifier of the topic to update

**Request Headers**:
- Authorization: Bearer {accessToken}
- Content-Type: application/json

**Request Body**:
```json
{
  "title": "Bank",
  "description": "Go to the bank to handle business",
  "level": "Beginner",
  "systemPrompt": "You are a bank clerk, and your job is to help customers handle business.",
  "start": "Hello! How can I help you today?"
}
```

**Field Descriptions**:
- `title`: Optional. The updated title of the topic
- `description`: Optional. Updated description of what will be learned
- `level`: Optional. Updated difficulty level of the topic (e.g., "Beginner")
- `systemPrompt`: Optional. Updated instructions for the AI system
- `start`: Optional. Updated initial message to start the conversation

**Success Response**:
- Status Code: 200 OK
```json
{
  "_id": {
    "$oid": "678559ac79bc79eeab784fe9"
  },
  "title": "Bank",
  "description": "Go to the bank to handle business",
  "level": "Beginner",
  "systemPrompt": "You are a bank clerk, and your job is to help customers handle business.",
  "start": "Hello! How can I help you today?",
  "createdAt": "2025-01-27T19:30:00Z",
  "user_id": {
    "$oid": "678ea72a7baff5011c1a27cf"
  }
}
```

**Error Response**:
- Status Code: 404 Not Found
```json
{
    "message": "Topic not found"
}
```
- Status Code: 401 Unauthorized
```json
{
    "message": "Authentication required"
}
```
- Status Code: 403 Forbidden
```json
{
    "message": "Not authorized to update this topic"
}
```
- Status Code: 400 Bad Request
```json
{
    "message": "Invalid topic data"
}
```

### Delete Topic

Deletes a specific topic by its ID.

**Endpoint**: `DELETE /api/topics/{topic_id}`

**Path Parameters**:
- `topic_id`: The unique identifier of the topic to delete

**Request Headers**:
- Authorization: Bearer {accessToken}
- Content-Type: application/json

**Success Response**:
- Status Code: 200 OK
```json
{
    "message": "Topic deleted successfully"
}
```

**Error Response**:
- Status Code: 404 Not Found
```json
{
    "message": "Topic not found"
}
```
- Status Code: 401 Unauthorized
```json
{
    "message": "Authentication required"
}
```
- Status Code: 403 Forbidden
```json
{
    "message": "Not authorized to delete this topic"
}
```


