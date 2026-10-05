# Web2App Kit — All Platforms Except macOS

This blueprint wraps a bundled website for Android, iOS, Windows, Linux, and Web/PWA. **macOS is explicitly excluded:** no macOS bundle, no `.icns`, no macOS workflow, and no release target.

| Platform | Runtime | Output |
|---|---|---|
| Android | Kotlin WebView | APK / AAB |
| iOS | Swift WKWebView | unsigned IPA/app artifact |
| Windows | Tauri 2 + WebView2 | MSIX / NSIS |
| Linux | Tauri 2 + WebKitGTK | AppImage / deb |
| Web | Browser | PWA static files |
| macOS | excluded | none |

## Shared conventions

- App identifier: `com.example.<slug>`.
- Version source: `version.json`.
- All wrappers bundle local assets from `app/site/`; never load a live URL by default.
- External navigation allowlist: `https`, `mailto`, `tel`, `sms`.
- Keep native bridges minimal; prefer localStorage/IndexedDB inside the WebView.

The `prompts/` directory contains detailed, copy-ready build prompts for each target and a no-macOS verification pass.
