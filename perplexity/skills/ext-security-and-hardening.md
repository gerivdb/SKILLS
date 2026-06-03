---
name: ext-security-and-hardening
version: "1.0.0"
description: "Security-first development practices (source: addyosmani/agent-skills). Harden code against vulnerabilities. Use when handling user input, authentication, data storage, or external integrations."
triggers: ["security", "vulnerability", "OWASP", "hardening", "input validation", "XSS", "CSRF", "injection"]
layer: "L2_COMPOSITION"
nexusTags: ["EXT_ADDYOSMANI"]
prerequisites: []
slotWeight: 1
status: active
upstream: https://github.com/addyosmani/agent-skills/blob/main/skills/security-and-hardening/SKILL.md
---
# ext-security-and-hardening

> Source: [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | Adapted for gerivdb/SKILLS

Security-first development practices for web applications. Treat every external input as hostile, every secret as sacred, and every authorization check as mandatory. Security isn't a phase - it's a constraint on every line of code.

## The Three-Tier Boundary System

### Always Do (No Exceptions)

- **Validate all external input** at the system boundary (API routes, form handlers)
- **Parameterize all database queries** - never concatenate user input into SQL
- **Encode output** to prevent XSS (use framework auto-escaping, don't bypass it)
- **Use HTTPS** for all external communication
- **Hash passwords** with bcrypt/scrypt/argon2 (never store plaintext)
- **Set security headers** (CSP, HSTS, X-Frame-Options, X-Content-Type-Options)
- **Use httpOnly, secure, sameSite cookies** for sessions
- **Run `npm audit`** (or equivalent) before every release

### Ask First (Requires Human Approval)

- Adding new authentication flows or changing auth logic
- Storing new categories of sensitive data (PII, payment info)
- Adding new external service integrations
- Changing CORS configuration
- Adding file upload handlers
- Modifying rate limiting or throttling
- Granting elevated permissions or roles

### Never Do

- **Never commit secrets** to version control (API keys, passwords, tokens)
- **Never log sensitive data** (passwords, tokens, full credit card numbers)
- **Never trust client-side validation** as a security boundary
- **Never disable security headers** for convenience
- **Never use `eval()` or `innerHTML`** with user-provided data
- **Never store sessions in client-accessible storage** (localStorage for auth tokens)
- **Never expose stack traces** or internal error details to users

## OWASP Top 10 Prevention

### 1. Injection (SQL, NoSQL, OS Command)
```typescript
// BAD: SQL injection via string concatenation
const query = `SELECT * FROM users WHERE id = '${userId}'`;

// GOOD: Parameterized query
const user = await db.query('SELECT * FROM users WHERE id = $1', [userId]);
```

### 2. Broken Authentication
- Passwords hashed with bcrypt/scrypt/argon2 (salt rounds >= 12)
- Sessions: httpOnly, secure, sameSite cookies
- Rate limiting on auth endpoints
- Password reset tokens: time-limited, single-use

### 3. Cross-Site Scripting (XSS)
```typescript
// BAD: Rendering user input as HTML
element.innerHTML = userInput;

// GOOD: Use framework auto-escaping (React does this by default)
return <div>{userInput}</div>;
```

### 4. Broken Access Control
- Authorization checked on every protected endpoint
- Users can only access their own resources (no IDOR)
- Admin actions require admin role verification

### 5. Security Misconfiguration
- Security headers: CSP, HSTS, X-Frame-Options
- CORS restricted to known origins
- Dependencies audited for known vulnerabilities
- Error messages don't expose internals

## Input Validation Patterns

Use schema validation at boundaries (e.g., Zod for TypeScript):

```typescript
const CreateTaskSchema = z.object({
  title: z.string().min(1).max(200).trim(),
  description: z.string().max(2000).optional(),
  priority: z.enum(['low', 'medium', 'high']).default('medium'),
});
```

## Triaging npm Audit Results

```
npm audit reports a vulnerability
├── Severity: critical or high
│   ├── Reachable in your app? -> Fix immediately
│   └── Dev-only/unused? -> Fix soon, not a blocker
├── Severity: moderate
│   └── Reachable in production? -> Fix in next release cycle
└── Severity: low
    └── Track and fix during regular dependency updates
```

## Security Review Checklist

```markdown
### Authentication
- [ ] Passwords hashed with bcrypt/scrypt/argon2 (salt rounds >= 12)
- [ ] Session tokens are httpOnly, secure, sameSite
- [ ] Login has rate limiting
- [ ] Password reset tokens expire

### Authorization
- [ ] Every endpoint checks user permissions
- [ ] Users can only access their own resources
- [ ] Admin actions require admin role verification

### Input
- [ ] All user input validated at the boundary
- [ ] SQL queries are parameterized
- [ ] HTML output is encoded/escaped

### Data
- [ ] No secrets in code or version control
- [ ] Sensitive fields excluded from API responses
- [ ] PII encrypted at rest (if applicable)

### Infrastructure
- [ ] Security headers configured (CSP, HSTS, etc.)
- [ ] CORS restricted to known origins
- [ ] Dependencies audited for vulnerabilities
- [ ] Error messages don't expose internals
```

## Integration with gerivdb

- Use `ext-security-auditor` agent for security review execution
- Complements: SABRE (security engine), ARGUS (governance audit)
- Gate: Security review required for L2+ repos before merge
- ENV2 specific: All secrets in `.env` files, never in code
