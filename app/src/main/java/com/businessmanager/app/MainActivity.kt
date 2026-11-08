
package com.businessmanager.app

import android.os.Bundle
import android.webkit.JavascriptInterface
import android.webkit.WebView
import androidx.appcompat.app.AppCompatActivity
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // Start Python
        if (!Python.isStarted()) {
            Python.start(AndroidPlatform(this))
        }

        // Setup WebView
        val webView = WebView(this)
        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true
        
        // Connect JS to Python
        webView.addJavascriptInterface(WebAppInterface(), "Android")
        
        // Load the UI
        webView.loadUrl("file:///android_asset/index.html")
        setContentView(webView)
    }

    // This class allows JavaScript to call Python
    inner class WebAppInterface {
        @JavascriptInterface
        fun callPython(method: String, jsonData: String): String {
            return try {
                val py = Python.getInstance().getModule("main")
                py.callAttr(method, jsonData).toString()
            } catch (e: Exception) {
                "{\"error\": \"${e.message}\"}"
            }
        }
    }
}
