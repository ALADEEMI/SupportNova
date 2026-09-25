# ADR-014 — Roles and access control

## Decision
Roles (SRS FR ii): `customer`, `agent`, `reviewer`, `manager`, `admin`. Permissions are data (`role_permissions`),
checked by `require_permission()` in services **and** page guards in UI (defense in depth).

| Capability | customer | agent | reviewer | manager | admin |
|---|:-:|:-:|:-:|:-:|:-:|
| Submit own complaint / view own | ✓ | | | | |
| Submit on behalf / batch import complaints | | ✓ | | | ✓ |
| View assigned complaint intelligence | | ✓ | ✓ | ✓ | ✓ |
| Change status, send approved response | | ✓ | ✓ | | ✓ |
| Manual review actions (8) | | | ✓ | | ✓ |
| Analytics, reports, export | | | | ✓ | ✓ |
| KB documents, rules, config, prompts, users | | | | | ✓ |
| Audit log viewer | | | | ✓ | ✓ |

Object-level rule: customers only ever see their own complaints (enforced in repository queries).
Passwords bcrypt-hashed; login lockout after N failed attempts (config); session idle timeout (config).
Seed accounts include `evaluator` (manager+reviewer view) and `admin` for Deliverable 15.

## SRS references
FR i–ii, NFR-3, Deliverable 10 (unauthorized-access tests), Deliverable 15.
