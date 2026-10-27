package org.example.energyblast.gdevelop;

import android.app.Activity;
import android.os.Bundle;
import android.net.Uri;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebSettings;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.util.Collections;
import java.util.Locale;

/** Small offline wrapper for the real exported GDevelop runtime; no WebView bridge. */
public final class MainActivity extends Activity {
    private static final String HOST = "energyblast.local";
    private WebView game;

    private static boolean local(Uri uri) {
        return "https".equals(uri.getScheme()) && HOST.equals(uri.getHost());
    }

    private static String mime(String path) {
        String extension = path.substring(path.lastIndexOf('.') + 1).toLowerCase(Locale.ROOT);
        switch (extension) {
            case "html": return "text/html";
            case "js": return "text/javascript";
            case "css": return "text/css";
            case "json": return "application/json";
            case "ogg": return "audio/ogg";
            case "png": return "image/png";
            case "svg": return "image/svg+xml";
            case "glb": return "model/gltf-binary";
            case "wasm": return "application/wasm";
            case "txt": return "text/plain";
            default: return "application/octet-stream";
        }
    }

    private WebResourceResponse blocked() {
        return new WebResourceResponse("text/plain", "UTF-8", 404, "Not Found",
                Collections.emptyMap(), new ByteArrayInputStream(new byte[0]));
    }

    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        game = new WebView(this);
        WebSettings settings = game.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true); // App-private persisted mission progress.
        settings.setAllowFileAccess(false);
        settings.setAllowContentAccess(false);
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        game.setWebViewClient(new WebViewClient() {
            @Override public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                return !local(request.getUrl());
            }
            @Override public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                Uri uri = request.getUrl();
                if (!local(uri) || !"GET".equals(request.getMethod())) return blocked();
                String path = uri.getPath();
                if (path == null || path.contains("..") || path.contains("\\")) return blocked();
                if ("/".equals(path)) path = "/index.html";
                try {
                    return new WebResourceResponse(mime(path), "UTF-8", getAssets().open(path.substring(1)));
                } catch (IOException error) { return blocked(); }
            }
        });
        setContentView(game);
        game.loadUrl("https://" + HOST + "/index.html");
    }
    @Override protected void onPause() {
        game.evaluateJavascript("document.dispatchEvent(new Event('energyblast-pause'))", null);
        game.onPause();
        super.onPause();
    }
    @Override protected void onResume() {
        super.onResume();
        if (game != null) {
            game.onResume();
            game.evaluateJavascript("document.dispatchEvent(new Event('energyblast-resume'))", null);
        }
    }
    @Override public void onBackPressed() {
        game.evaluateJavascript("globalThis.__energyblast && globalThis.__energyblast.menu()", null);
    }
    @Override protected void onDestroy() {
        game.destroy();
        super.onDestroy();
    }
}
