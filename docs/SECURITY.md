<<<<<<< HEAD
# Security considerations

This document describes the current local-development implementation. It is not a production security certification.

## Authentication and authorization

- Passwords are hashed by the backend. Login returns a signed JWT access token; protected API calls validate the access-token type and resolve the user.
- The frontend stores the access token in `localStorage`. A cross-site scripting flaw could expose it, so keep dependencies current and avoid unsafe HTML rendering.
- Registration permits driver and passenger roles, not admin. Backend dependencies enforce role requirements, with ownership checks on user-owned resources.
- Google/GitHub OAuth is optional and disabled until server credentials are configured. The callback uses a short-lived state cookie, requests identity-only scopes, requires verified provider email, and stores unique provider subjects. It links only to an existing CommuteShare account with that verified email; OAuth does not create accounts.
- Password-reset links use random tokens whose SHA-256 digest and expiration are stored in the user record. Requests use a generic response for known and unknown accounts, and are throttled per account. SMTP credentials must stay in the ignored local `.env`; mail is delivered only when SMTP is configured. Reset does not send SMS.
- Resetting a password does not revoke already-issued stateless JWTs; those remain valid until their configured expiration.

## Secrets and local configuration

- Never commit a real `.env`, JWT key, database password, private key, user upload, or database dump.
- `backend/.env.example` is a local Compose example. It includes `DEBUG=True`, a placeholder `SECRET_KEY`, and development database credentials. Do not deploy those values.
- For any deployment, supply a strong unique secret and database credential through a deployment-specific secret mechanism. This repository does not provision one.

## Uploads, maps, and safety

- Avatar images are stored on the backend filesystem and served by the `/uploads` mount. A production multi-instance storage and retention policy is not configured.
- The map sends requests to the configured tile service; the default is OpenStreetMap's public tile endpoint. Follow its [tile policy](https://operations.osmfoundation.org/policies/tiles/), retain visible attribution, and do not bulk-download tiles.
- SOS creates an in-app record and notifies configured admin users. It does not contact emergency services; the UI should not be treated as an emergency dispatch channel.
- Payment rows are status tracking only. There is no payment processor or card-data handling flow.

## Deployment boundary

The Compose file binds local ports to loopback, but its development settings, credentials, and reload server are not suitable for public deployment. The repository has no AWS infrastructure or production TLS, backup, monitoring, or network configuration. See [Deployment notes](DEPLOYMENT.md).

No private security contact is configured in the repository. If reporting a vulnerability, contact the maintainer privately rather than publishing exploit details in a public issue.
=======
# 🔐 CommuteShare Security

Security is an important part of the CommuteShare architecture.

As a platform that handles user accounts, authentication, ride information, bookings, payments, notifications, and emergency events, CommuteShare applies multiple security practices across the frontend, backend, API, and database layers.

This document explains the security mechanisms currently implemented in the project and recommended improvements for future production deployment.

---

## 📋 Table of Contents

* [Security Overview](#-security-overview)
* [Security Architecture](#-security-architecture)
* [Authentication](#-authentication)
* [Password Security](#-password-security)
* [JWT Security](#-jwt-security)
* [Authorization and RBAC](#-authorization-and-rbac)
* [Ownership Validation](#-ownership-validation)
* [API Security](#-api-security)
* [Input Validation](#-input-validation)
* [Database Security](#-database-security)
* [CORS Security](#-cors-security)
* [Audit Logging](#-audit-logging)
* [SOS and Safety Events](#-sos-and-safety-events)
* [Environment Security](#-environment-security)
* [Docker Security](#-docker-security)
* [Security Testing](#-security-testing)
* [Threat Considerations](#-threat-considerations)
* [Future Security Improvements](#-future-security-improvements)
* [Security Checklist](#-security-checklist)

---

# 🛡️ Security Overview

CommuteShare uses a defense-in-depth approach.

Security controls exist across multiple layers of the application.

```text id="sec-overview"
┌─────────────────────────────────────┐
│            Frontend                 │
│                                     │
│ • Protected Routes                  │
│ • Client-side validation            │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│             API Layer               │
│                                     │
│ • JWT Authentication                │
│ • Request validation                │
│ • Authorization checks              │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│          Business Logic             │
│                                     │
│ • RBAC                              │
│ • Ownership validation              │
│ • Workflow validation               │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│           Database Layer            │
│                                     │
│ • Foreign keys                      │
│ • Constraints                       │
│ • Referential integrity             │
└─────────────────────────────────────┘
```

The main security goals are:

* Protect user accounts
* Protect passwords
* Prevent unauthorized access
* Enforce user permissions
* Protect application data
* Maintain auditability
* Validate user input
* Reduce common API security risks

---

# 🏗️ Security Architecture

The application security flow follows this pattern:

```text id="security-flow"
User Request
     │
     ▼
Frontend
     │
     │ HTTPS / HTTP Request
     ▼
FastAPI Endpoint
     │
     ▼
Authentication
     │
     ├── Invalid Token ─────► Reject
     │
     ▼
Authorization
     │
     ├── Insufficient Role ─► Reject
     │
     ▼
Ownership Validation
     │
     ├── Not Owner ─────────► Reject
     │
     ▼
Input Validation
     │
     ├── Invalid Input ─────► Reject
     │
     ▼
Business Logic
     │
     ▼
Database
```

Each layer provides additional protection.

---

# 🔑 Authentication

CommuteShare uses token-based authentication.

The authentication system allows users to:

* Register an account
* Log in
* Receive an access token
* Access protected endpoints
* Identify the authenticated user

---

## Authentication Flow

```text id="auth-flow"
User
 │
 │ Email + Password
 ▼
Login Endpoint
 │
 ▼
Find User
 │
 ▼
Verify Password
 │
 ├── Invalid ─────► Reject Request
 │
 ▼
Generate JWT
 │
 ▼
Return Access Token
 │
 ▼
Frontend Stores Authentication State
 │
 ▼
Protected API Requests
 │
 ▼
Authorization: Bearer <token>
```

Protected endpoints require a valid authentication token.

Example:

```http id="auth-header"
Authorization: Bearer <access_token>
```

---

# 🔒 Password Security

Passwords should never be stored as plain text.

CommuteShare stores a password hash instead of the original password.

```text id="password-security"
User Password
      │
      ▼
Password Hashing
      │
      ▼
Password Hash
      │
      ▼
Database
```

During login:

```text id="password-verification"
User Password
      │
      ▼
Password Verification
      │
      ├── Incorrect ─────► Reject
      │
      ▼
Password Matches Stored Hash
      │
      ▼
Authentication Successful
```

This ensures that database records do not contain users' original passwords.

---

# 🎟️ JWT Security

JSON Web Tokens are used to identify authenticated users.

A token contains information used by the backend to verify the request.

```text id="jwt-structure"
JWT

Header
  │
Payload
  │
Signature
```

The backend verifies the token before allowing access to protected resources.

---

## Token Validation

Before processing a protected request:

```text id="token-validation"
Request
   │
   ▼
Extract Token
   │
   ▼
Verify Signature
   │
   ├── Invalid ─────► 401 Unauthorized
   │
   ▼
Check Expiration
   │
   ├── Expired ─────► 401 Unauthorized
   │
   ▼
Extract User Identity
   │
   ▼
Continue Request
```

---

## JWT Secret

The JWT secret must be stored securely.

Example:

```env id="jwt-secret"
SECRET_KEY=your_long_random_secret
```

The secret should:

* Be long and randomly generated
* Never be hardcoded in source code
* Never be committed to Git
* Be different between development and production
* Be rotated if compromised

---

# 👥 Authorization and RBAC

CommuteShare uses Role-Based Access Control (RBAC).

The application defines user roles such as:

```text id="roles"
Admin
Driver
Passenger
```

Each role is allowed to perform specific actions.

---

## Example Permissions

| Action             | Passenger | Driver | Admin |
| ------------------ | --------: | -----: | ----: |
| View rides         |         ✅ |      ✅ |     ✅ |
| Create ride        |         ❌ |      ✅ |     ✅ |
| Register vehicle   |         ❌ |      ✅ |     ✅ |
| Book ride          |         ✅ |      ✅ |     ❌ |
| Manage own ride    |         ❌ |      ✅ |     ❌ |
| Manage users       |         ❌ |      ❌ |     ✅ |
| View platform data |         ❌ |      ❌ |     ✅ |

Authorization checks occur on the backend.

> ⚠️ Frontend route protection improves the user experience but must not be treated as the primary security boundary.

The backend remains responsible for enforcing permissions.

---

# 👤 Ownership Validation

Role checks alone are not enough.

The application also verifies ownership when users perform actions on specific resources.

Examples:

```text id="ownership-examples"
User
 │
 ├── Can modify their own profile
 │
 ├── Can manage their own vehicle
 │
 ├── Can manage their own ride
 │
 └── Can manage their own booking
```

Example:

```text id="ownership-flow"
User Requests Ride Update
        │
        ▼
Find Ride
        │
        ▼
Compare ride.driver_id
with current_user.id
        │
        ├── Different ─────► 403 Forbidden
        │
        ▼
Allow Update
```

This helps prevent **IDOR (Insecure Direct Object Reference)** vulnerabilities.

---

# 🌐 API Security

The backend uses REST APIs.

Important API security practices include:

* Authentication dependencies
* Authorization checks
* Input validation
* Ownership validation
* Structured error responses
* Protected administrative routes
* Controlled request schemas

Example request flow:

```text id="api-security"
HTTP Request
     │
     ▼
FastAPI Route
     │
     ▼
Authentication Dependency
     │
     ▼
Authorization Check
     │
     ▼
Pydantic Validation
     │
     ▼
Business Logic
     │
     ▼
Database
```

---

# 🧾 Input Validation

CommuteShare uses Pydantic schemas for request validation.

Schemas help validate:

* Required fields
* Data types
* Optional fields
* Numeric ranges
* Structured request data

Example:

```text id="validation-flow"
Incoming JSON
      │
      ▼
Pydantic Schema
      │
      ├── Invalid ─────► Validation Error
      │
      ▼
Validated Data
      │
      ▼
Application Logic
```

Validation reduces the risk of:

* Invalid application states
* Unexpected input
* Type-related errors
* Malformed API requests

---

# 🗄️ Database Security

The database uses relational integrity mechanisms.

Security-related database controls include:

* Primary keys
* Foreign keys
* Unique constraints
* Check constraints
* Controlled enum values

Examples:

```text id="db-security"
users.email
    │
    └── UNIQUE

vehicles.registration_number
    │
    └── UNIQUE

booking(passenger_id, ride_id)
    │
    └── UNIQUE

rating
    │
    └── CHECK 1 ≤ rating ≤ 5
```

These constraints help prevent invalid or duplicate data even if an application-level validation issue occurs.

---

# 🌍 CORS Security

Cross-Origin Resource Sharing (CORS) controls which frontend origins can access the backend.

Development example:

```text id="cors-dev"
http://localhost:5173
```

Production environments should restrict allowed origins.

Example:

```env id="cors-prod"
BACKEND_CORS_ORIGINS=["https://yourdomain.com"]
```

Avoid using unrestricted origins in production:

```text id="cors-warning"
*
```

unless there is a specific and carefully reviewed requirement.

---

# 📝 Audit Logging

Audit logs help record important system and security events.

Examples include:

* User registration
* User login
* Ride creation
* Ride updates
* Booking creation
* Booking cancellation
* Administrative actions
* Security-related events

---

## Audit Flow

```text id="audit-flow"
User Action
     │
     ▼
Application Event
     │
     ▼
Audit Service
     │
     ▼
Audit Log Entry
     │
     ├── User
     ├── Action
     ├── Resource
     ├── Description
     ├── IP Address
     └── Timestamp
```

Audit logs support:

* Troubleshooting
* Incident investigation
* Security monitoring
* Administrative review

---

# 🆘 SOS and Safety Events

CommuteShare includes an SOS event system.

An SOS event can record:

* User information
* Associated ride
* Emergency type
* Description
* Geographic coordinates
* Event status
* Timestamp

---

## SOS Flow

```text id="sos-security-flow"
User
 │
 │ Trigger SOS
 ▼
SOS API Endpoint
 │
 ▼
Authenticate User
 │
 ▼
Validate Request
 │
 ▼
Create SOS Event
 │
 ▼
Record Timestamp
 │
 ▼
Store Event
 │
 ▼
Authorized Review
```

SOS events may contain sensitive information.

Future production versions should consider:

* Restricted access controls
* Data retention policies
* Encryption where appropriate
* Administrative review
* Emergency contact workflows

---

# ⚙️ Environment Security

Sensitive configuration should be stored in environment variables.

Examples:

```env id="env-security"
DATABASE_URL=postgresql://...
SECRET_KEY=...
```

The `.env` file should not be committed to Git.

Recommended `.gitignore` entry:

```text id="gitignore-security"
.env
*.env
```

A safe example configuration file can be provided as:

```text id="env-example"
.env.example
```

Example:

```env id="env-example-content"
DATABASE_URL=postgresql://username:password@localhost/database
SECRET_KEY=change_me
```

Real credentials must never be included in `.env.example`.

---

# 🐳 Docker Security

Docker improves deployment consistency, but container security should still be considered.

Recommended practices:

* Use minimal base images
* Keep dependencies updated
* Avoid embedding secrets in images
* Use environment variables for configuration
* Run containers with minimal privileges
* Scan images for vulnerabilities
* Avoid running containers as root when possible

Example future security workflow:

```text id="docker-security"
Source Code
     │
     ▼
Docker Build
     │
     ▼
Dependency Scan
     │
     ▼
Container Scan
     │
     ▼
Deploy
```

---

# 🧪 Security Testing

Security testing can be performed at multiple levels.

## Authentication Testing

Test:

* Invalid credentials
* Missing token
* Invalid token
* Expired token
* Access to protected routes

---

## Authorization Testing

Test:

* Passenger accessing driver endpoints
* Passenger accessing admin endpoints
* Driver accessing admin endpoints
* Unauthorized resource modification

---

## Ownership Testing

Test scenarios such as:

```text id="ownership-testing"
User A creates Ride
        │
        ▼
User B attempts modification
        │
        ▼
Expected Result
        │
        ▼
403 Forbidden
```

---

## Input Validation Testing

Test:

* Missing fields
* Invalid data types
* Invalid enum values
* Negative values
* Invalid ratings
* Malformed JSON

---

# ⚠️ Threat Considerations

The following threats should be considered when developing and deploying CommuteShare.

---

## Broken Authentication

Potential risks:

* Weak passwords
* Token theft
* Token expiration issues

Mitigations:

* Password hashing
* JWT expiration
* Authentication dependencies
* Future refresh token support

---

## Broken Access Control

Potential risks:

* Unauthorized resource access
* Privilege escalation
* IDOR vulnerabilities

Mitigations:

* Backend authorization checks
* RBAC
* Ownership validation
* Protected admin endpoints

---

## Injection Attacks

Potential risks:

* SQL injection
* Malicious input

Mitigations:

* SQLAlchemy ORM
* Parameterized queries
* Pydantic validation
* Avoiding unsafe raw SQL

---

## Sensitive Data Exposure

Potential risks:

* Exposed environment variables
* Exposed database credentials
* Weak production configuration

Mitigations:

* Environment variables
* `.gitignore`
* Secret management
* HTTPS in production

---

## Denial of Service

Potential risks:

* Excessive API requests
* Automated attacks
* Resource exhaustion

Future mitigations:

* Rate limiting
* Request size limits
* Reverse proxy controls
* Monitoring

---

## Dependency Vulnerabilities

Potential risks:

* Outdated Python packages
* Outdated Node.js packages
* Vulnerable container images

Future mitigations:

* Dependency scanning
* Dependabot
* Automated security updates
* Container image scanning

---

# 🚀 Future Security Improvements

The following improvements can strengthen CommuteShare for production use.

---

## Authentication

* [ ] Refresh tokens
* [ ] Refresh token rotation
* [ ] Token revocation
* [ ] Secure logout
* [ ] Password reset workflow
* [ ] Email verification
* [ ] Two-factor authentication

---

## API Protection

* [ ] Rate limiting
* [ ] Request throttling
* [ ] API versioning
* [ ] Request size limits
* [ ] Security headers
* [ ] API monitoring

---

## Account Security

* [ ] Login attempt tracking
* [ ] Account lockout
* [ ] Suspicious login detection
* [ ] Device/session tracking
* [ ] Account recovery workflows

---

## Infrastructure

* [ ] HTTPS enforcement
* [ ] Reverse proxy
* [ ] Web Application Firewall
* [ ] Centralized logging
* [ ] Intrusion monitoring
* [ ] Automated backups
* [ ] Disaster recovery strategy

---

## Security Automation

Future CI/CD security pipeline:

```text id="security-pipeline"
Developer Push
      │
      ▼
GitHub Actions
      │
      ├── Code Quality
      │
      ├── Unit Tests
      │
      ├── Dependency Scan
      │
      ├── Static Analysis
      │
      └── Container Scan
                │
                ▼
             Deploy
```

Potential tools:

* Dependabot
* Bandit
* Safety
* Trivy
* Checkov
* Semgrep

---

# ✅ Security Checklist

Before production deployment:

### Authentication

* [x] Password hashing
* [x] JWT authentication
* [x] Protected endpoints
* [ ] Refresh tokens
* [ ] Token revocation

### Authorization

* [x] RBAC
* [x] Ownership validation
* [x] Protected admin operations

### API

* [x] Request validation
* [x] Structured schemas
* [ ] Rate limiting
* [ ] Security headers

### Database

* [x] Foreign keys
* [x] Unique constraints
* [x] Check constraints
* [ ] Automated backups

### Infrastructure

* [x] Docker support
* [ ] HTTPS enforcement
* [ ] Reverse proxy
* [ ] Container vulnerability scanning

### Monitoring

* [x] Audit logs
* [x] Security event records
* [ ] Centralized logging
* [ ] Alerting

---

# ⚠️ Security Disclaimer

CommuteShare is a learning and portfolio project.

The security mechanisms documented here demonstrate common application security practices, but the project should undergo additional security testing, threat modelling, dependency review, infrastructure hardening, and production security assessment before being used in a real-world production environment.

---

# 📚 Related Documentation

| Document             | Description                       |
| -------------------- | --------------------------------- |
| `ARCHITECTURE.md`    | Overall application architecture  |
| `DATABASE_SCHEMA.md` | Database design and relationships |
| `API_REFERENCE.md`   | REST API documentation            |
| `DEPLOYMENT.md`      | Deployment instructions           |
| `ROADMAP.md`         | Future project improvements       |

---

<div align="center">

### 🔐 Security Is Not a Feature. It's a Foundation.

**CommuteShare Security Documentation**

</div>
>>>>>>> origin/main
