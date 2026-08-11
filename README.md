## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
  - [1. Upload Flow](#1-upload-flow)
  - [2. Chat Flow](#2-chat-flow)
  - [3. Feedback Flow](#3-feedback-flow)
- [Diagram](#diagram)

## Overview

The system is built around three core flows:

1. **Upload** – ingesting a user's file, storing it, and preparing it for retrieval.
2. **Chat** – routing a user's question to the right agent, retrieving relevant context, and generating an answer.
3. **Feedback** – capturing whether the generated answer was useful.

## Architecture

### 1. Upload Flow

1. User uploads a file.
2. File metadata (name, size, owner, timestamp, etc.) is saved into the database.
3. The file itself is stored in a folder (file storage).
4. The file is extracted (text/content extraction).
5. Extracted content is divided into chunks.
6. Each chunk is embedded and stored in a vector store for retrieval.

### 2. Chat Flow

1. User sends a request containing a question.
2. The request passes through a **router**.
3. The router detects and forwards the request to the respective **agent**.
4. The agent checks whether a **tool** is required to answer the question.
   - If yes, the tool is invoked.
   - If no, it proceeds directly to retrieval.
5. The agent retrieves relevant data from the stored chunks (vector store).
6. The agent generates and returns an answer to the user.

### 3. Feedback Flow

1. User submits feedback on the generated answer.
2. Feedback indicates whether the response was useful or not.
3. Feedback is stored in the database for future analysis/improvement.

### 4. Diagram
![architecture](docs\arch-final.png)