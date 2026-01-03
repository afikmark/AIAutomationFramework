---
agent: Git Agent
---
# Git Operations Prompt

Perform git operations following best practices and conventional commit standards.

## Workflow:

### Pre-Commit Phase
1. **Check Status**: Run `git status` to see current changes
2. **Review Changes**: Use `git diff` to review modifications
3. **Validate Quality**:
   - Ensure tests are passing
   - Verify no sensitive data (credentials, .env files)
   - Check for proper formatting
   - Confirm code follows repository conventions

### Staging Phase
4. **Stage Files**: 
   - Stage specific files: `git add <file1> <file2>`
   - Stage all changes: `git add -A` (use cautiously)
   - Interactive staging: `git add -p` (for selective staging)

### Commit Phase
5. **Write Commit Message** following Conventional Commits format:
   ```
   <type>(<scope>): <subject>
   
   <body - optional but recommended>
   
   <footer - optional: issues, breaking changes>
   ```

   **Commit Types:**
   - `feat`: New features
   - `fix`: Bug fixes
   - `test`: Test additions/updates
   - `docs`: Documentation
   - `refactor`: Code refactoring
   - `chore`: Maintenance tasks
   - `style`: Formatting changes
   - `perf`: Performance improvements

   **Example:**
   ```
   feat(agents): add Git Agent for version control operations
   
   - Created GitAgent.md with comprehensive git workflow
   - Added git-operations.md prompt template
   - Includes conflict resolution strategies
   - Follows VS Code custom agent conventions
   
   Related: Code review integration
   ```

6. **Commit**: `git commit -m "your message"`

### Push Phase
7. **Pre-Push Validation**:
   - Verify tests pass: `pytest`
   - Check branch name: `git branch --show-current`
   - Ensure clean merge: `git pull --rebase origin <branch>` (if needed)

8. **Push Changes**:
   - New branch: `git push -u origin <branch-name>`
   - Existing branch: `git push origin <branch-name>`
   - To master: **Only after code review approval**

## Conflict Resolution:

If conflicts occur during pull/merge:

1. **Identify Conflicts**: `git status` shows conflicted files
2. **Review Conflict Markers**:
   ```
   <<<<<<< HEAD
   Your changes
   =======
   Incoming changes
   >>>>>>> branch-name
   ```
3. **Choose Resolution Strategy**:
   - Accept current (HEAD)
   - Accept incoming (branch)
   - Merge both changes
   - Custom manual resolution

4. **Resolve and Test**:
   ```bash
   # Edit conflicted files
   git add <resolved-files>
   git commit -m "resolve: merge conflicts in <component>"
   pytest  # Verify functionality
   ```

## Branch Management:

**Creating Branches:**
```bash
# Feature branch
git checkout -b feature/new-cart-functionality

# Bug fix branch
git checkout -b fix/cart-badge-display

# Test branch
git checkout -b test/comprehensive-cart-coverage
```

**Branch Cleanup:**
```bash
# Delete local branch
git branch -d <branch-name>

# Delete remote branch
git push origin --delete <branch-name>
```

## Safety Guidelines:

⚠️ **Before Committing:**
- [ ] Tests are passing
- [ ] No debug code or console.logs
- [ ] No commented-out code (unless explained)
- [ ] No credentials or API keys
- [ ] No .env files or local configuration
- [ ] Commit message is clear and descriptive

⚠️ **Before Pushing to Master:**
- [ ] Code has been reviewed
- [ ] All tests passing in CI/CD (if applicable)
- [ ] Documentation updated
- [ ] Breaking changes communicated
- [ ] Team approval obtained

⚠️ **Never Do:**
- Force push to shared branches: `git push --force` (use `--force-with-lease` if needed)
- Commit large binary files
- Commit generated files (unless necessary)
- Push directly to master without review
- Rewrite public history

## Common Scenarios:

### Scenario 1: Stage and commit reviewed code
```bash
git status
git add .github/agents/GitAgent.md .github/prompts/git-operations.md
git commit -m "feat(agents): add Git Agent for version control operations"
git push origin feature/add-git-agent
```

### Scenario 2: Commit test additions
```bash
git add tests/sauce_ui/test_cart_page.py
git commit -m "test(cart): add 8 new test functions for cart page

- Covers DEV-40, DEV-33, DEV-32, DEV-39, DEV-36, DEV-41, DEV-38, DEV-34
- Tests cart display, navigation, persistence, and browser interactions
- All 25 tests passing"
git push origin test/cart-page-coverage
```

### Scenario 3: Resolve merge conflict
```bash
git pull origin main
# CONFLICT in file.py
# Edit file.py to resolve conflicts
git add file.py
git commit -m "resolve: merge conflicts in file.py"
pytest tests/
git push origin feature/my-branch
```

### Scenario 4: Amend last commit
```bash
# Forgot to add a file
git add forgotten-file.py
git commit --amend --no-edit
git push --force-with-lease origin feature/my-branch
```

## Quick Reference:

| Task | Command |
|------|---------|
| Check status | `git status` |
| View changes | `git diff` |
| Stage file | `git add <file>` |
| Stage all | `git add -A` |
| Commit | `git commit -m "message"` |
| Push | `git push origin <branch>` |
| Pull | `git pull origin <branch>` |
| Create branch | `git checkout -b <branch>` |
| Switch branch | `git checkout <branch>` |
| View log | `git log --oneline -10` |
| Undo staging | `git reset HEAD <file>` |
| Discard changes | `git checkout -- <file>` |
| Stash changes | `git stash` |
| Apply stash | `git stash pop` |

Execute git operations with these guidelines to maintain a clean, professional repository history.
