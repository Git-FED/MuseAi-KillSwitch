# No-macOS verification prompt

Audit the repository. `macos-latest` is permitted only for the iOS build job. Tauri targets must contain no `dmg`, `app`, or Apple target. No `.icns` files may exist. No macOS build workflow, no live URL loading, and no README claim that macOS is supported. Re-run the audit and report every remaining violation as a one-line diff.
