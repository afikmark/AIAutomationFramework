# Feature Documentation Template

Use this template to document features for the Test Creator Agent.

## Feature Name - [Component/Page] Documentation

### Overview
Brief description of what this feature/page does and its purpose in the application.

### URL & Navigation
How users access this feature:
- URL path or route
- Navigation steps from other pages
- Entry points

### Layout & Design (Optional)
Visual/structural elements if relevant for testing:
- Key UI components
- Form elements
- Buttons and actions

### Behavioral Logic & User Flows

#### Normal/Happy Path Flow
1. Step 1: User action
2. Step 2: System response
3. Step 3: Expected result
4. ...

#### Error/Validation Cases
List all error scenarios:
- **Scenario description** → Expected error message/behavior
- **Another scenario** → Expected error message/behavior
- **Edge case** → Expected behavior

### Valid Input Data
Document what constitutes valid input:
- Field name: Valid format/values description
- Field name: Valid format/values description
- Valid credentials (if applicable)
- Valid user types/roles

### Invalid Input Data
Document what should be rejected:
- Field name: Invalid formats that should fail
- Field name: Invalid values that should be rejected
- Invalid credentials description
- Edge cases description

### Expected Outcomes

#### Success Criteria
What indicates successful operation:
- UI changes description
- Navigation/redirects description
- Data changes description
- Visual feedback description

#### Failure Indicators
What indicates operation failed:
- Error messages description
- No state change description
- Visual indicators description

### Performance & Timing Notes (Optional)
Any timing considerations:
- Expected load times
- Timeout behaviors
- Async operations

### Test Coverage Requirements
What should be tested:
- ✅ Happy path with valid data
- ✅ Each error case
- ✅ Boundary conditions
- ✅ Permission/role variations
- ✅ State transitions

### Known Issues or Special Behaviors (Optional)
Any quirks, workarounds, or special handling needed.

---

## Documentation Quality Guidelines

**Be Specific:**
- Use exact error messages, not vague descriptions
- Provide actual data formats and values
- Document precise UI element names

**Cover Comprehensively:**
- All possible user flows
- All error scenarios
- All validation rules
- Edge cases and boundary conditions

**Structure Consistently:**
- Follow the template sections
- Use consistent terminology
- Maintain clear hierarchies

**Maintain Currency:**
- Keep synchronized with application changes
- Update when features change
- Document new behaviors promptly

## How the Agent Uses This Documentation

The Test Creator Agent will:
1. Read the documentation to understand expected behavior
2. Extract test scenarios from documented flows
3. Use valid/invalid data patterns in tests
4. Verify features are documented before generation
5. Generate assertions based on success/failure criteria

**Remember:** The better the documentation, the better the generated tests!
