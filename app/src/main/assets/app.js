
// Initialize DB on load
if (window.Android) {
    window.Android.callPython("init_db", "{}");
}

function addSale() {
    if (!window.Android) return alert("Run inside APK");
    const data = JSON.stringify({ amount: 100, date: new Date().toISOString().split('T')[0] });
    window.Android.callPython("add_sale", data);
    getSales();
}

function getSales() {
    if (!window.Android) return;
    const res = JSON.parse(window.Android.callPython("get_sales", "{}"));
    
    const list = document.getElementById("sales-list");
    const totalSpan = document.getElementById("total-sales");
    
    if (res.sales && res.sales.length > 0) {
        list.innerHTML = "";
        let total = 0;
        res.sales.forEach(sale => {
            total += sale.amount;
            list.innerHTML += `<li><span>${sale.date}</span> <b>+₹${sale.amount}</b></li>`;
        });
        totalSpan.innerText = "₹" + total;
    }
}

function generatePDF() {
    if (!window.Android) return alert("Run inside APK");
    const res = JSON.parse(window.Android.callPython("generate_pdf", "{}"));
    alert("PDF Saved to: " + res.path);
}

// Initial load
getSales();
