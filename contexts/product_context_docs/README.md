# context_docs/ - Product Documentation

## Purpose

This folder contains **product/feature documentation only** - what the application does from a user's perspective.

**Use this folder for:**
- ✅ Feature specifications
- ✅ Expected behavior
- ✅ Valid/invalid inputs
- ✅ Error messages
- ✅ User workflows
- ✅ Business rules

**Do NOT use this folder for:**
- ❌ Implementation details
- ❌ Code patterns
- ❌ Architecture documentation
- ❌ Testing strategies
- ❌ Technical how-tos

## What Goes Here

### Example: Login Feature Documentation ✅

```markdown
# Login Page Documentation

## Valid Credentials
- Username: standard_user
- Password: secret_sauce

## Error Cases
- Empty username → "Username is required"
- Wrong password → "Username and password do not match"
- Locked user → "Sorry, this user has been locked out"
```

This describes **what the product does**, not **how to test it**.

### Example: What NOT to Put Here ❌

```markdown
# How to Use LocatorProvider
Use fetch_locators_with_fallback()...
```

This is technical implementation - belongs in root-level `.md` files.

## File Naming Convention

Use descriptive names that match the feature:
- `saucedemo_login_page.md` - Login page behavior
- `shopping_cart.md` - Shopping cart functionality
- `checkout_flow.md` - Checkout process

Avoid technical names like:
- ❌ `locator_pattern.md`
- ❌ `page_objects.md`
- ❌ `test_structure.md`

## How the Agent Uses This

The Test Creator Agent reads these docs to understand:
1. **What features exist** - Can only generate tests for documented features
2. **Expected behavior** - What should happen in success/error cases
3. **Valid test data** - What inputs are valid/invalid
4. **Feature boundaries** - What's in scope for testing

## Adding New Documentation

1. Create a new `.md` file in this folder
2. Follow the TEMPLATE.md structure (in root directory)
3. Focus on user-facing behavior, not implementation
4. Include all error cases and edge conditions
5. Restart the agent to load new documentation

## Separation of Concerns

```
context_docs/               # WHAT the product does
  ├── login_page.md        # Product behavior
  └── shopping_cart.md     # Feature specs

root directory/             # HOW to implement
  ├── locator_provider_pattern.md    # Technical patterns
  └── TEMPLATE.md                     # Doc template
```

**Remember:** Product managers, QA, and non-technical team members should be able to write documentation for this folder. If it requires coding knowledge, it doesn't belong here!
