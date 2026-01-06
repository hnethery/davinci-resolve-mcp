## 2025-01-20 - Smart Polling in CLI Tools
**Learning:** Users perceive "waiting" time differently when there is no feedback. A fixed `sleep 10` is a poor experience because it punishes fast users (who start the app in 2s) and fails slow users (who take 11s).
**Action:** Replace fixed sleeps with smart polling loops (short sleep + check) and visual feedback (e.g., dots or spinner). This minimizes wait time and provides confidence that the system is working. Use a timeout to prevent infinite loops.
