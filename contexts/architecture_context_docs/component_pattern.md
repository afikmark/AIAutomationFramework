# Component Pattern

## Overview

Components are reusable UI elements that appear across multiple pages in the application. Unlike page objects that represent entire pages, components represent smaller, self-contained UI elements like menus, modals, navigation bars, or any repeating UI pattern.

## When to Use Components

Create a component when:
- ✅ The UI element appears on multiple pages (hamburger menu, navigation bar)
- ✅ The UI element is a self-contained widget (modal, dropdown, accordion)
- ✅ The element has its own set of interactions separate from the page
- ✅ You want to reuse the same interaction logic across different pages

Don't create a component when:
- ❌ The element is page-specific and doesn't appear elsewhere
- ❌ The element is a simple single-purpose button or input
- ❌ The element is tightly coupled to a single page's business logic

**Components are:**
- Reusable UI elements that appear across multiple pages
- Composed into page objects as properties
- Focused on a single UI widget or element

**Components are NOT:**
- Complete pages (use page objects for that)
- Navigation-focused (no goto() methods)
- Test containers (tests use components through page objects)

Use components to reduce duplication and maintain consistency when the same UI element appears in multiple places in your application.
