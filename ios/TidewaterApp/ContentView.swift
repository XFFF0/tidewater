import SwiftUI
@preconcurrency import WebKit

final class DebugModel: ObservableObject {
    @Published var lines: [String] = []
    @Published var beat: String = "hb: none yet"
    @Published var visible = true

    func add(_ s: String) {
        DispatchQueue.main.async {
            if s.hasPrefix("hb ") { self.beat = s; return }
            self.lines.append(s)
            if self.lines.count > 14 { self.lines.removeFirst() }
        }
    }
}

final class LogHandler: NSObject, WKScriptMessageHandler {
    let model: DebugModel
    init(model: DebugModel) { self.model = model }
    func userContentController(_ c: WKUserContentController, didReceive m: WKScriptMessage) {
        if let s = m.body as? String { model.add(s) }
    }
}

struct ContentView: View {
    @StateObject private var model = DebugModel()
    private let sha = (Bundle.main.infoDictionary?["BuildSHA"] as? String) ?? "?"

    var body: some View {
        ZStack(alignment: .topLeading) {
            WebView(model: model)
                .ignoresSafeArea()
                .background(Color.black)
            if model.visible {
                VStack(alignment: .leading, spacing: 2) {
                    Text("build \(sha) | \(model.beat) | tap to hide")
                    ForEach(Array(model.lines.enumerated()), id: \.offset) { item in
                        Text(item.element).lineLimit(2)
                    }
                }
                .font(.system(size: 10, design: .monospaced))
                .foregroundColor(.green)
                .frame(maxWidth: 520, alignment: .leading)
                .padding(6)
                .background(Color.black.opacity(0.7))
                .padding(.top, 8)
                .padding(.leading, 60)
                .onTapGesture { model.visible = false }
            }
        }
    }
}

private let debugScript = #"""
(function(){
  function send(s){ try{ window.webkit.messageHandlers.log.postMessage(String(s)); }catch(e){} }
  ['log','info','warn','error'].forEach(function(k){
    var o = console[k].bind(console);
    console[k] = function(){
      try{
        send(k + ': ' + Array.prototype.map.call(arguments, function(a){
          try{ return (a && a.stack) || (typeof a === 'object' ? JSON.stringify(a) : String(a)); }catch(e){ return String(a); }
        }).join(' ').slice(0,300));
      }catch(e){}
      o.apply(null, arguments);
    };
  });
  window.addEventListener('error', function(e){ send('ERR ' + e.message + ' @' + String(e.filename||'').split('/').pop() + ':' + e.lineno); });
  window.addEventListener('unhandledrejection', function(e){ var r = e.reason; send('REJ ' + ((r && (r.stack || r.message)) || r)); });
  var frames = 0, last = 0, raf = window.requestAnimationFrame.bind(window);
  window.requestAnimationFrame = function(cb){ return raf(function(t){ frames++; cb(t); }); };
  send('gpu=' + (!!navigator.gpu) + ' touch=' + ('ontouchstart' in window) + ' ua=' + navigator.userAgent.slice(0,50));
  if (navigator.gpu) {
    navigator.gpu.requestAdapter().then(function(a){ send('adapter=' + (a ? 'ok' : 'null')); }).catch(function(e){ send('adapterErr ' + e); });
  }
  setInterval(function(){ send('hb frames=' + frames + ' (+' + (frames - last) + '/s)'); last = frames; }, 1000);
})();
"""#

struct WebView: UIViewRepresentable {
    let model: DebugModel

    func makeUIView(context: Context) -> WKWebView {
        let config = WKWebViewConfiguration()
        config.allowsInlineMediaPlayback = true
        config.mediaTypesRequiringUserActionForPlayback = []

        // diagnostics: console + errors + frame heartbeat -> native overlay
        let ucc = config.userContentController
        ucc.add(LogHandler(model: model), name: "log")
        ucc.addUserScript(WKUserScript(source: debugScript, injectionTime: .atDocumentStart, forMainFrameOnly: true))

        // no long-press image menu / Live Text / Visual Look Up on the game canvas
        config.preferences.isTextInteractionEnabled = false

        let webView = WKWebView(frame: .zero, configuration: config)
        webView.isOpaque = false
        webView.backgroundColor = .black
        webView.scrollView.bounces = false
        webView.scrollView.isScrollEnabled = false
        webView.allowsBackForwardNavigationGestures = false
        webView.allowsLinkPreview = false

        if let indexURL = Bundle.main.url(forResource: "index", withExtension: "html", subdirectory: "dist") {
            let baseURL = indexURL.deletingLastPathComponent()
            webView.loadFileURL(indexURL, allowingReadAccessTo: baseURL.deletingLastPathComponent())
        } else {
            model.add("ERR dist/index.html not found in bundle")
        }

        return webView
    }

    func updateUIView(_ uiView: WKWebView, context: Context) {}
}
