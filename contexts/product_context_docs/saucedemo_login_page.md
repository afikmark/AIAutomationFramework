# SauceDemo / Swag Labs — Login Page Documentation

## Overview

The Login Page is the gateway entry point to the Swag Labs (SauceDemo) application. Users must authenticate here before accessing the inventory (product) area. The page contains the form inputs for username/password, branding, supporting hints, and error handling behavior.

## URL & Navigation

| Environment | URL / Path | Notes |
|------------|------------|-------|
| Production / Demo | https://www.saucedemo.com/ | Root landing → login page. |

When a user accesses the root domain, they land immediately on the login page if not authenticated. Upon successful login, the user is redirected to `/inventory.html`.

## Layout & Design

### Branding & Header

- At the top center is the Swag Labs logo / brand name (text/logo).
- The general page background is light / off-white / very pale grey (almost white) to maintain contrast with form elements.
- The login form is centrally aligned both vertically and horizontally (on wider screens).
- Beneath (or aside) the form, there is a footer-style box showing "Accepted usernames are:" and "Password for all users:" with credential hints.

## Behavioral Logic & UX Flow

### Normal Flow (Successful Login)

1. User visits the login page (root URL).
2. They enter username + password.
3. They click the Login button (or press Enter in a field).
4. System validates credentials.
5. If correct, user is redirected to `/inventory.html`.
6. The inventory page loads, showing product listings.

### Error / Validation Cases (Login Fails)

If login fails (for any of the invalid scenarios), the page displays an error message near the form and **DOES NOT redirect to inventory**. Common failure cases:

- **Empty username or password** — show "Username is required" or "Password is required" (or a general "Username and password required")
- **Invalid credentials** (non-existent user or wrong password) — show "Username and password do not match any user"
- **Locked out user** (`locked_out_user`) — show "Sorry, this user has been locked out."

These error messages appear dynamically (often in a red-highlighted error box) and prevent navigation. The input fields remain editable so user can correct input. **The user remains on the login page; the URL does not change.**

Many test scenarios around the login page revolve around these negative flows.

### Edge / UX Enhancements

- The password input is masked (●●●) by default; sometimes there may be an option to unmask (not in base demo).
- Hitting Enter in either input field triggers form submission (same as clicking login).
- After a failed login, the state remains on the login page; the URL does not change.
- On successful login, if the user bookmarks an internal page and then logs out, the user may be redirected back to login.
- The credential hint box (with accepted usernames/password) is always visible to support testers/users.

## Performance & Timing Notes

- The `performance_glitch_user` is a **VALID user** that successfully logs in, but with intentional performance delays
- Test scripts using `performance_glitch_user` should allow extra timeouts for page transitions
- No aggressive client-side caching / redirect logic is present on the login page itself
- The login operation is synchronous (i.e. form submit triggers server validation) — there is no multi-step handshake visible from UI

## Supported Credential Sets (Testing / Demo)

The demo site documents several special users. **All use the same password: `secret_sauce`**

### Valid Users (Successfully Authenticate & Redirect to Inventory)

| Username | Behavior | Expected Outcome |
|----------|----------|------------------|
| `standard_user` | Normal user with no special behavior | ✅ Successful login → redirects to `/inventory.html` |
| `performance_glitch_user` | Valid user with intentional performance delays | ✅ Successful login → redirects to `/inventory.html` (after delay) |
| `problem_user` | Valid user that may encounter UI glitches on other pages | ✅ Successful login → redirects to `/inventory.html` |

### Invalid Users (Authentication Fails & Shows Error)

| Username | Behavior | Expected Outcome |
|----------|----------|------------------|
| `locked_out_user` | User account is locked/disabled | ❌ Login fails → shows "Sorry, this user has been locked out." |
| Any non-existent username | User doesn't exist in system | ❌ Login fails → shows "Username and password do not match any user" |
| Valid username + wrong password | Incorrect password | ❌ Login fails → shows "Username and password do not match any user" |
| Empty username or password | Missing required field | ❌ Login fails → shows "Username is required" or "Password is required" |

## Test Coverage Requirements

### Critical Test Scenarios

**Successful Login Tests:**
- ✅ Valid login with `standard_user` → verify redirect to `/inventory.html`
- ✅ Valid login with `performance_glitch_user` → verify redirect to `/inventory.html` (with appropriate wait/timeout)
- ✅ Valid login with `problem_user` → verify redirect to `/inventory.html`

**Failed Login Tests (Error Scenarios):**
- ❌ Attempt login with `locked_out_user` → expect error "locked out" and NO redirect
- ❌ Attempt login with invalid credentials (random username or wrong password) → expect error "do not match" and NO redirect
- ❌ Attempt login with empty username → expect error "Username is required" and NO redirect
- ❌ Attempt login with empty password → expect error "Password is required" and NO redirect

**State Management Tests:**
- Error message appears on failed login
- Error message clears/disappears on successful login after failure
- Username field retains value after failed login (password field may be cleared)

### Test Design Guidelines

- **Group by outcome**: All failed login scenarios can be parametrized together (empty fields, wrong credentials, locked user)
- **Separate performance tests**: `performance_glitch_user` should have its own test with appropriate timeouts
- **Separate success tests**: Successful logins should be tested separately from error cases (different assertions)
