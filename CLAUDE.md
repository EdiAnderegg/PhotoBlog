# PhotoBlog

## Project Purpose

PhotoBlog is an MVP photography portfolio website for a hobby photographer.

The primary goal of the MVP is to present photography beautifully and allow visitors to discover photography collections and contact the photographer.

This is currently a portfolio/content website, not an e-commerce platform.

## MVP Scope

The MVP supports:

- A visually focused homepage.
- Browsing published photography collections.
- Viewing a photography collection and its photographs.
- Viewing an individual photograph.
- Photographer biography/about information.
- Instagram and contact information.
- Photographer content management through Django Admin.

Explicitly out of scope for the MVP:

- Payments.
- Shopping carts.
- Customer accounts.
- Paid downloads.
- Merchandise.
- Licensing.
- Customer order management.

Do not introduce out-of-scope functionality unless explicitly requested.

## Technology Stack

Backend and server-rendered frontend:

- Python
- Django
- Django Templates

Database:

- PostgreSQL

Application server:

- Gunicorn

Reverse proxy:

- Nginx

Infrastructure:

- Docker
- Docker Compose

Target production environment:

- Single Hetzner Cloud server.

## Infrastructure Architecture

The intended deployment topology is:

Client
-> Nginx
-> Gunicorn
-> Django
-> PostgreSQL

Nginx is the public entry point.

PostgreSQL must not be exposed publicly.

Development should maintain production-like topology where practical.

Avoid adding infrastructure unless there is a demonstrated requirement.

Do not introduce:

- Kubernetes
- Redis
- Celery
- message brokers
- microservices
- separate frontend SPA frameworks

unless explicitly requested and justified.

## Domain Language

### Collection

A curated photography story, theme, style, location, or scenario.

Examples:

- St. Petersburg After Rain
- Faces of Summer
- Quiet Places

A Collection contains multiple Photos.

### Photo

A photograph belonging to a Collection.

A Photo may contain:

- title
- description
- alt text
- image
- publication status
- display order
- optional capture date
- optional location

### Photographer

The person publishing the photography portfolio.

The photographer manages content through Django Admin in the MVP.

## Media Storage

Image binary data must not be stored directly inside PostgreSQL.

Use Django ImageField/FileField and a storage backend.

The database should contain the storage-relative file path/reference.

Do not hardcode full public image URLs into domain models.

Development may initially use persistent filesystem storage.

The storage implementation should remain replaceable so object storage can be introduced later.

## Engineering Principles

Prefer the simplest implementation that satisfies the current requirement.

Apply:

- YAGNI
- KISS
- separation of concerns
- explicit domain terminology
- maintainability

Do not introduce abstractions merely because they may become useful later.

Do not create separate architectural layers unless they have a concrete responsibility.

Django conventions should be preferred over unnecessary custom infrastructure.

## Development Workflow

Work from one GitHub issue at a time.

For each issue:

1. Read and restate the acceptance criteria.
2. Inspect the existing implementation.
3. Identify the smallest vertical slice required.
4. Propose an implementation plan before making substantial changes.
5. Implement only the approved scope.
6. Add or update relevant tests.
7. Run relevant tests.
8. Run the complete test suite before considering the issue finished.
9. Summarize the changes and remaining concerns.

Do not create Git commits unless explicitly asked.

Do not silently expand the scope of an issue.

Do not add a new dependency without explaining why it is needed.

## Testing Strategy

Primary test runner:

- pytest

Django integration:

- pytest-django

BDD / acceptance scenarios:

- pytest-bdd

Use Given / When / Then acceptance tests for meaningful user-visible behavior.

Do not force every acceptance criterion into a BDD test.

### Unit Tests

Use unit tests for meaningful isolated behavior such as:

- domain rules
- validation
- ordering rules
- transformations
- services containing business logic

Do not unit-test trivial Django framework behavior.

### Integration Tests

Use integration tests when behavior crosses boundaries such as:

- Django ORM + PostgreSQL
- views + database
- forms + models
- file storage
- Django Admin behavior

### Acceptance Tests

Acceptance tests describe externally observable product behavior.

Example:

Given a published collection contains published photographs
When a visitor opens the collection
Then the published photographs are displayed in their configured order

Acceptance scenarios should describe business behavior rather than implementation details.

## Testing Rule During Implementation

When modifying behavior:

- identify which existing tests should protect the behavior
- add a failing test first when practical
- implement the smallest change that satisfies the test
- refactor only after tests pass

After implementation, run the relevant test scope.

Before completing an issue, run the entire test suite.

## Code Quality

Keep functions and classes focused.

Prefer descriptive domain names over generic technical names.

Avoid unnecessary inheritance and generic repository patterns unless they solve a real problem.

Do not manually edit generated Django migrations unless explicitly required.

Use Django migrations for schema changes.

Keep secrets out of source control.

Use environment variables for production-sensitive configuration.
