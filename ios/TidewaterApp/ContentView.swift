import SwiftUI
@preconcurrency import WebKit

struct ContentView: View {
    var body: some View {
        WebView()
            .ignoresSafeArea()
            .background(Color.black)
    }
}

struct WebView: UIViewRepresentable {
    func makeUIView(context: Context) -> WKWebView {
        let config = WKWebViewConfiguration()
        config.allowsInlineMediaPlayback = true
        config.mediaTypesRequiringUserActionForPlayback = []

        // WebGPU support (on by default in recent WebKit, force it on for older builds).
        let prefs = config.preferences
        prefs.setValue(true, forKey: "developerExtrasEnabled")
        for key in ["WebGPUEnabled", "webGPUEnabled"] {
            if config.responds(to: NSSelectorFromString("_setPreferences:")) {
                config.preferences.setValue(true, forKey: key)
            }
        }

        // no long-press image menu / Live Text / Visual Look Up on the game canvas
        config.preferences.isTextInteractionEnabled = false

        let webView = WKWebView(frame: .zero, configuration: config)
        webView.configuration.preferences.isTextInteractionEnabled = false
        webView.isOpaque = false
        webView.backgroundColor = .black
        webView.scrollView.bounces = false
        webView.scrollView.isScrollEnabled = false
        webView.allowsBackForwardNavigationGestures = false
        webView.allowsLinkPreview = false

        if let indexURL = Bundle.main.url(forResource: "index", withExtension: "html", subdirectory: "dist") {
            let baseURL = indexURL.deletingLastPathComponent()
            webView.loadFileURL(indexURL, allowingReadAccessTo: baseURL.deletingLastPathComponent())
        }

        return webView
    }

    func updateUIView(_ uiView: WKWebView, context: Context) {}
}
