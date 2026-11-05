# Antigravity implementation prompt

You are working inside the existing GrowthIQ repository. Read README.md and docs/PROJECT_BRIEF.md first.

The project is a portfolio case study using synthetic fashion e-commerce data. Never claim that the data is actual CAVA data.

Tasks:
1. Inspect the repository and run the app in a local Python environment.
2. Fix any dependency, runtime, data, or SQL issues you find.
3. Add automated data-quality tests: primary-key uniqueness, foreign-key integrity, non-negative quantities/prices, valid funnel event names, and no order item without an order.
4. Add a data-quality page or section with row counts, null rates, duplicate checks, and referential integrity results.
5. Add campaign-level performance, month-over-month changes, discount-band performance, and a first-touch vs last-touch attribution comparison where the available synthetic data supports it.
6. Improve dashboard layout, filters, chart labels, empty states, and accessibility. Keep the visual identity refined: warm ivory, deep burgundy, muted taupe, restrained gold accents.
7. Add a downloadable CSV export for filtered tables and a concise generated insights section. Every insight must be calculated from the filtered data and labelled as simulated.
8. Run tests and provide exact commands and results. Do not fabricate successful test results.
9. Update README with any new features and limitations.

Do not replace the stack or remove existing functionality without explaining why. Work incrementally and keep the app runnable after each change.
