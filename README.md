# 🔗 Serverless URL Shortener (API Gateway + Lambda + DynamoDB)

A fully serverless URL Shortener — similar to Bit.ly — built using **AWS API Gateway**, **AWS Lambda**, and **Amazon DynamoDB**.  
This project converts long URLs into short codes and redirects users instantly.

🚀 **Perfect portfolio project for anyone transitioning into AWS Cloud.**

---

## 📌 Features

- Shortens any long URL into a unique short ID  
- Redirects users via HTTP **302**  
- Uses a fully **serverless backend**  
- DynamoDB used as a fast NoSQL key-value store  
- API Gateway exposes clean REST endpoints  
- Zero servers to manage, auto-scaling, pay-per-use  

---

## 🏗️ Architecture

1. **POST /shorten**  
   - Lambda generates a random short ID  
   - Saves `{ shortId, longUrl }` into DynamoDB  
   - Returns the full short URL

2. **GET /{shortId}**  
   - Lambda looks up the long URL from DynamoDB  
   - Returns a **302 redirect** to the destination URL

**Services used:**
- AWS Lambda  
- Amazon DynamoDB  
- Amazon API Gateway  
- IAM Roles & Permissions  

---

## 🚀 API Endpoints

### 1️⃣ **Create Short URL**
`POST /shorten`

#### Example Request:
```json
{
  "url": "https://google.com"
}
