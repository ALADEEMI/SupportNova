# 01 — Organization Profile: Zephyra Electronics (fictional)

> Fictional company created for the competition (SRS Step 1, CI-01). No real customer data is used.

## 1. Company
- **Name:** Zephyra Electronics
- **Industry:** Online retail of smart-home and personal electronics, with subscription and installation services.
- **Channels:** website, mobile app, email, live chat (channels are complaint metadata only — SRS 1.4 excludes live integrations).
- **Currency:** USD. **Timezone:** UTC (display in browser local time).

## 2. Product catalog (≈40 products seeded; categories below)
| Product category | Examples | Why it matters |
|---|---|---|
| Smartphones | Zephyra Z9, Z9 Lite | defects, warranty, high value |
| Laptops | AeroBook 14, AeroBook Pro 16 | high-value disputes |
| Tablets | ZenPad X2 | overheating/battery |
| Audio | PulseBuds, PulseBuds Pro | returns, DOA |
| Smart Home Security | HomeEye Cam, SafeLock Smart Lock | privacy, security |
| Personal Mobility | GlideOne E-Scooter | battery fire / injury (safety) |
| Smart Kitchen | CrispAir Fryer | overheating / burn (safety) |
| Wearables | Pulse Watch 3 | subscription features |

## 3. Services
| Service | Type | Complaint exposure |
|---|---|---|
| **ZenCare** protection plan | monthly/annual subscription | renewal, cancellation, claims |
| **Zephyra Cloud** | camera recording storage subscription | privacy, renewal |
| Home Installation | booked service (installers) | staff misconduct, damage |
| Trade-in | device buy-back | valuation disputes |
| Express Delivery | paid delivery option | delay, fee refund |
| Installments ("PayLater") | payment plan | installment billing issues |

## 4. Customer types (configurable)
`Standard`, `Plus` (ZenCare/Cloud subscriber), `VIP` (top spenders), `Business` (B2B accounts).
Customer type is stored on the customer profile — never self-declared on the complaint form.

## 5. Complaint taxonomy (12 categories, 26 subcategories — seeded, configurable)
| Category | Subcategories | Primary department |
|---|---|---|
| Delivery | Delayed Delivery; Lost Shipment; Wrong Item Delivered; Damaged in Transit | Logistics |
| Product Defect | Dead on Arrival; Malfunction After Use | Technical Support |
| Billing | Duplicate Charge; Incorrect Charge; Installment Issue | Billing & Payments |
| Refund | Refund Delay; Refund Denial Dispute | Billing & Payments |
| Returns & Replacement | Return Request; Replacement Request | Returns & Replacements |
| Warranty | Warranty Claim; Repair Delay | Warranty & Repairs |
| Subscription | Unwanted Renewal; Cancellation Issue | Subscriptions |
| Account & Security | Account Takeover; Access Issue | Account Security |
| Privacy | Data Exposure; Recording Privacy Concern | Privacy & Compliance |
| Product Safety | Overheating / Fire Risk; Injury / Electric Shock | Product Safety |
| Technical Support | Setup & Connectivity; App / Firmware Issue | Technical Support |
| Service Quality | Staff Misconduct; Poor Support Experience | Customer Relations |

## 6. Departments (11, configurable)
Logistics · Technical Support · Billing & Payments · Returns & Replacements · Warranty & Repairs · Subscriptions ·
Account Security · Privacy & Compliance · Product Safety · Customer Relations · Management Escalations.
Legal-threat complaints add **Privacy & Compliance** as supporting department (compliance handles legal).

## 7. Fixed vocabularies from the SRS (seeded as configuration)
- Sentiment (Step 17): Positive, Neutral, Negative, Strongly Negative
- Emotion indicators (Step 18): Frustration, Anger, Disappointment, Confusion, Urgency
- Urgency (Step 19): Low, Medium, High, Critical
- Priority (Step 20): P3 – Low, P2 – Medium, P1 – High, P0 – Critical
- Escalation levels (Step 37): No Escalation, Supervisor Review, Department Manager, Specialist Team, Compliance Review, Critical Management Escalation
- Statuses (Step 60): New, Analyzed, Assigned, In Progress, Awaiting Customer, Escalated, Resolved, Closed, Reopened
- Response tones (Step 33): Professional, Empathetic, Concise, Formal
- Follow-up types (Step 40): Request for Additional Information, Resolution Confirmation, Refund-Status Update, Replacement-Status Update, Escalation Acknowledgement, Closure Confirmation
- Policy applicability (Step 26): Applicable, Conditionally Applicable, Not Applicable, Outdated
- Document statuses (Step 7): Active, Previous, Superseded, Draft
- Complaint channels (1.2): Web Form, Email, Chat, Messaging, Customer Portal, Uploaded Complaint
- Requested resolutions: Refund, Replacement, Repair, Compensation, Cancellation, Information, Apology, Other

## 8. Knowledge-base documents (24 doc codes, 29 files incl. old versions)
| Doc code | Title | Category | Versions (status) | Format |
|---|---|---|---|---|
| ZEP-POL-001 | Complaint Handling Policy | Policy | v1.0 Active | DOCX |
| ZEP-POL-002 | Customer Service Standards | Policy | v1.0 Active | PDF |
| ZEP-POL-003 | Refund Policy | Policy | v2.0 Superseded; v3.0 Active | DOCX, PDF |
| ZEP-POL-004 | Returns & Replacement Policy | Policy | v2.0 Active | PDF |
| ZEP-POL-005 | Order Cancellation Policy | Policy | v1.0 Active | DOCX |
| ZEP-POL-006 | Billing & Payments Policy | Policy | v1.0 Superseded; v2.0 Active | PDF |
| ZEP-POL-007 | Delivery Policy | Policy | v2.0 Active | DOCX |
| ZEP-POL-008 | Warranty Policy | Policy | v1.0 Active | PDF |
| ZEP-POL-009 | Privacy & Data Protection Policy | Policy | v1.0 Active | DOCX |
| ZEP-POL-010 | Product Safety Incident Policy | Policy | v2.0 Active | PDF |
| ZEP-POL-011 | Compensation & Goodwill Policy | Policy | v1.0 Active; v2.0 Draft | DOCX |
| ZEP-POL-012 | Subscription Terms (ZenCare & Zephyra Cloud) | Policy | v1.0 Active | PDF |
| ZEP-POL-013 | Account Security Policy | Policy | v1.0 Active | DOCX |
| ZEP-SLA-001 | Service Level Agreement | SLA | v1.0 Active | PDF |
| ZEP-ESC-001 | Escalation Procedure | Escalation Procedure | v2.0 Active | DOCX |
| ZEP-SOP-001 | Complaint Triage SOP | SOP | v1.0 Superseded (conflicting); v2.0 Active | PDF |
| ZEP-SOP-002 | Refund Processing SOP | SOP | v1.0 Active | DOCX |
| ZEP-SOP-003 | Safety Incident SOP | SOP | v1.0 Active | PDF |
| ZEP-RTG-001 | Department Routing Rules | Routing Rules | v1.0 Active | DOCX |
| ZEP-GDL-001 | Product Support Guidelines | Guidelines | v1.0 Active | PDF |
| ZEP-CMP-001 | Compliance & Legal Handling Guidelines | Guidelines | v1.0 Active | DOCX |
| ZEP-TPL-001 | Response Templates | Response Templates | v1.0 Active | DOCX |
| ZEP-FAQ-001 | Customer FAQ | FAQ | v1.0 Active (contains conflicts) | PDF |
| ZEP-PRC-001 | Document Precedence Rules | Policy | v1.0 Active | DOCX |

## 9. Deliberate knowledge conflicts (drive ≥20 contradictory complaint cases)
| ID | Conflict | Resolution by precedence |
|---|---|---|
| KC-01 | FAQ: refund window 14 days — Refund Policy v3 §3.1: 30 days | Policy wins (30) |
| KC-02 | Triage SOP v1 (superseded): safety → Supervisor — Safety Policy v2 §3.1: Critical Management within 2h | Active policy wins |
| KC-03 | Billing Policy v1 (superseded): duplicate refund in 14 days — v2 §4.2: 5 business days | Active v2 |
| KC-04 | FAQ: "free replacement any time" — Returns & Replacement §4: conditions apply | Policy wins |
| KC-05 | FAQ: next-day delivery — Delivery Policy §2.1: 2–4 business days (express: 1–2) | Policy wins |
| KC-06 | Compensation v2 (Draft) allows 20% credit — v1 Active allows max 10% goodwill with supervisor approval | Draft never used |
| KC-07 | FAQ omits liquid-damage exclusion — Warranty §5.3 excludes it | Policy wins |
| KC-08 | Response Templates: cancel ZenCare 3 days before renewal — Subscription Terms §6.2: 7 days | Policy wins over template |

## 10. Key policy facts the rules will encode (to be written into the documents)
- Refund: 30 days from delivery, unused/original packaging, or confirmed defect (Refund Policy v3 §3).
- Safety incidents: stop-use instruction, safety case, Critical Management Escalation within 2 hours; refund/replacement only after inspection (Safety Policy §3).
- Privacy/data exposure: Compliance Review mandatory; 72-hour internal notification (Privacy §4).
- Account takeover: lock account immediately, Account Security, Specialist Team escalation (Account Security §3).
- High-value dispute: order amount ≥ 1,000 USD → Department Manager review (Escalation Procedure §3).
- Repeat unresolved (≥2 prior unresolved on same order/product) → Supervisor Review minimum (Escalation Procedure §4).
- Legal threat language → Compliance Review + supporting Privacy & Compliance (Compliance Guidelines §2).
- Goodwill compensation ≤10% of order value, requires supervisor approval; never promised in first response (Compensation v1 §2).
- Replacement: within 30 days if defect confirmed; one replacement per order; not for physical/liquid damage (Returns & Replacement §4).
- Warranty: 12 months (24 for laptops), excludes liquid and physical damage (Warranty §2, §5).
- SLA (SLA §2): P0 respond 1h/resolve 24h · P1 4h/48h · P2 24h/5d · P3 48h/10d.
