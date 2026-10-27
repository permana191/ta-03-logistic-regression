document.addEventListener("DOMContentLoaded", function () {
    
    // =========================================
    // 1. LOGIKA TOMBOL FORM & LOADING SPINNER
    // =========================================
    const form = document.getElementById("predictForm");
    const submitBtn = document.getElementById("submitBtn");
    const btnText = document.getElementById("btnText");
    const btnSpinner = document.getElementById("btnSpinner");

    if (form) {
        form.addEventListener("submit", function () {
            // Menonaktifkan tombol agar tidak di-klik 2 kali
            submitBtn.disabled = true;
            submitBtn.classList.add("opacity-80", "cursor-not-allowed");
            
            // Mengubah tampilan tombol menjadi muter (spinner)
            btnText.style.display = "none";
            btnSpinner.classList.remove("hidden");
        });
    }

    // =========================================
    // 2. RENDER GRAFIK CHART.JS (Jika ada hasil)
    // =========================================
    if (isSubmitted && typeof Chart !== 'undefined') {
        
        // Konfigurasi Warna berdasarkan status risiko
        const gaugeColor = statusClass === 'danger' ? '#ef4444' : '#10b981'; // Merah atau Hijau
        const gaugeTrackColor = '#e2e8f0';

        // --- A. GAUGE CHART (Doughnut Setengah) ---
        const ctxGauge = document.getElementById('riskGauge').getContext('2d');
        new Chart(ctxGauge, {
            type: 'doughnut',
            data: {
                labels: ['Risiko', 'Aman'],
                datasets: [{
                    data: [riskProbability, 100 - riskProbability],
                    backgroundColor: [gaugeColor, gaugeTrackColor],
                    borderWidth: 0,
                    borderRadius: [10, 0], // Membuat ujung melengkung
                }]
            },
            options: {
                rotation: -90, // Memutar dari atas ke kiri
                circumference: 180, // Hanya setengah lingkaran
                cutout: '80%', // Ketebalan garis
                plugins: {
                    legend: { display: false },
                    tooltip: { enabled: false }
                },
                maintainAspectRatio: false,
                animation: {
                    animateRotate: true,
                    duration: 1500,
                    easing: 'easeOutQuart'
                }
            }
        });

        // --- B. RADAR CHART (Company vs Industry) ---
        const ctxRadar = document.getElementById('radarChart').getContext('2d');
        new Chart(ctxRadar, {
            type: 'radar',
            data: {
                labels: ['ROA(C)', 'Debt Ratio', 'Net Income', 'Working Cap', 'Cash'],
                datasets: [
                    {
                        label: 'Input Perusahaan',
                        data: [
                            formDataJS.roa, 
                            formDataJS.debt, 
                            formDataJS.netIncome, 
                            formDataJS.workingCap, 
                            formDataJS.cash
                        ],
                        backgroundColor: 'rgba(37, 99, 235, 0.2)', // Biru Transparan
                        borderColor: 'rgba(37, 99, 235, 1)',
                        pointBackgroundColor: 'rgba(37, 99, 235, 1)',
                        borderWidth: 2
                    },
                    {
                        label: 'Standar Aman Industri',
                        // Nilai rata-rata patokan perusahaan yang tidak bangkrut
                        data: [0.55, 0.10, 0.85, 0.80, 0.15],
                        backgroundColor: 'rgba(16, 185, 129, 0.1)', // Hijau Transparan
                        borderColor: 'rgba(16, 185, 129, 0.5)',
                        borderDash: [5, 5],
                        pointRadius: 0,
                        borderWidth: 1.5
                    }
                ]
            },
            options: {
                scales: {
                    r: {
                        angleLines: { color: 'rgba(0, 0, 0, 0.05)' },
                        grid: { color: 'rgba(0, 0, 0, 0.05)' },
                        pointLabels: {
                            font: { size: 10, family: "'Inter', sans-serif" },
                            color: '#64748b'
                        },
                        ticks: { display: false } // Sembunyikan angka di jaring
                    }
                },
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { boxWidth: 12, font: { size: 10 } }
                    }
                },
                maintainAspectRatio: false
            }
        });
    }
});

// =========================================
// 3. FUNGSI TOMBOL DEMO (Bantuan Input Cepat)
// =========================================
function fillDemoData(type) {
    if (type === 'aman') {
        document.getElementById('roa').value = 0.53;
        document.getElementById('debt_ratio').value = 0.12;
        document.getElementById('net_income').value = 0.84;
        document.getElementById('working_capital').value = 0.82;
        document.getElementById('cash_assets').value = 0.08;
    } else if (type === 'bahaya') {
        // Angka yang condong ke perusahaan bangkrut
        document.getElementById('roa').value = 0.35;
        document.getElementById('debt_ratio').value = 0.22;
        document.getElementById('net_income').value = 0.65;
        document.getElementById('working_capital').value = 0.60;
        document.getElementById('cash_assets').value = 0.01;
    }
}