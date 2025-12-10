// Dummy hierarchical data for testing (replace with AMD4 CSV / backend API)
const data = [
    {
        province: "DKI Jakarta",
        cities: [
            {
                city: "Jakarta Barat",
                districts: [
                    {
                        district: "Kembangan",
                        subdistricts: ["Kembangan Utara", "Kembangan Selatan"]
                    },
                    {
                        district: "Grogol Petamburan",
                        subdistricts: ["Grogol", "Tomang"]
                    }
                ]
            },
            {
                city: "Jakarta Pusat",
                districts: [
                    {
                        district: "Gambir",
                        subdistricts: ["Gambir Utara", "Gambir Selatan"]
                    }
                ]
            }
        ]
    },
    {
        province: "Jawa Barat",
        cities: [
            {
                city: "Bandung",
                districts: [
                    {
                        district: "Coblong",
                        subdistricts: ["Dago", "Lebakgede"]
                    }
                ]
            }
        ]
    }
];

// debug
console.log('script.js loaded');

const _debugBtn = document.getElementById('checkFlood');
if (!_debugBtn) {
    console.error('checkFlood button not found in DOM');
} else {
    _debugBtn.addEventListener('click', () => {
        console.log('checkFlood clicked');
    });
}
// References to dropdowns
const provinceSelect = document.getElementById("province");
const citySelect = document.getElementById("city");
const districtSelect = document.getElementById("district");
const subdistrictSelect = document.getElementById("subdistrict");
const resultsDiv = document.getElementById("results");

// Populate provinces
data.forEach(p => {
    const opt = document.createElement("option");
    opt.value = p.province;
    opt.textContent = p.province;
    provinceSelect.appendChild(opt);
});

// On province change
provinceSelect.addEventListener("change", () => {
    citySelect.innerHTML = '<option value="">Select City</option>';
    districtSelect.innerHTML = '<option value="">Select District</option>';
    subdistrictSelect.innerHTML = '<option value="">Select Subdistrict</option>';
    districtSelect.disabled = true;
    subdistrictSelect.disabled = true;

    const selectedProvince = data.find(p => p.province === provinceSelect.value);
    if (!selectedProvince) {
        citySelect.disabled = true;
        return;
    }

    selectedProvince.cities.forEach(c => {
        const opt = document.createElement("option");
        opt.value = c.city;
        opt.textContent = c.city;
        citySelect.appendChild(opt);
    });
    citySelect.disabled = false;
});

// On city change
citySelect.addEventListener("change", () => {
    districtSelect.innerHTML = '<option value="">Select District</option>';
    subdistrictSelect.innerHTML = '<option value="">Select Subdistrict</option>';
    subdistrictSelect.disabled = true;

    const selectedProvince = data.find(p => p.province === provinceSelect.value);
    const selectedCity = selectedProvince.cities.find(c => c.city === citySelect.value);
    if (!selectedCity) {
        districtSelect.disabled = true;
        return;
    }

    selectedCity.districts.forEach(d => {
        const opt = document.createElement("option");
        opt.value = d.district;
        opt.textContent = d.district;
        districtSelect.appendChild(opt);
    });
    districtSelect.disabled = false;
});

// On district change
districtSelect.addEventListener("change", () => {
    subdistrictSelect.innerHTML = '<option value="">Select Subdistrict</option>';
    const selectedProvince = data.find(p => p.province === provinceSelect.value);
    const selectedCity = selectedProvince.cities.find(c => c.city === citySelect.value);
    const selectedDistrict = selectedCity.districts.find(d => d.district === districtSelect.value);
    if (!selectedDistrict) {
        subdistrictSelect.disabled = true;
        return;
    }

    selectedDistrict.subdistricts.forEach(s => {
        const opt = document.createElement("option");
        opt.value = s;
        opt.textContent = s;
        subdistrictSelect.appendChild(opt);
    });
    subdistrictSelect.disabled = false;
});

// ...existing code...
document.getElementById("checkFlood").addEventListener("click", async () => {
    // use option text (displayed/canonical name) instead of option value (which was ADM code)
    const province = provinceSelect.options[provinceSelect.selectedIndex]?.text.trim() || provinceSelect.value;
    const city = citySelect.options[citySelect.selectedIndex]?.text.trim() || citySelect.value;
    const district = districtSelect.options[districtSelect.selectedIndex]?.text.trim() || districtSelect.value;
    const subdistrict = subdistrictSelect.options[subdistrictSelect.selectedIndex]?.text.trim() || subdistrictSelect.value; // canonical kelurahan

    if (!province || !city || !district || !subdistrict) {
        resultsDiv.textContent = "Please select all fields!";
        return;
    }

    resultsDiv.textContent = "Requesting backend prediction...";

    try {
        const resp = await fetch("http://localhost:5000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ kelurahan: subdistrict, province, city, district })
        });

        if (!resp.ok) {
            const txt = await resp.text().catch(() => "");
            throw new Error(`Server ${resp.status}: ${txt}`);
        }

        const json = await resp.json();
        if (json.error) {
            resultsDiv.textContent = `Backend error: ${json.error}`;
            return;
        }

        const rows = json.results || [];
        if (rows.length === 0) {
            resultsDiv.innerHTML = `<strong>No results for ${subdistrict}</strong>`;
            return;
        }

        let html = `<h3>Predictions for ${subdistrict}</h3><div class="pred-list">`;
        rows.forEach((r, i) => {
            html += `
                <div class="pred-item">
                    <strong>Forecast ${i+1}</strong>
                    <div>Date/Time: ${r.datetime}</div>
                    <div>Weather: ${r.weather ?? "-"}</div>
                    <div>Temperature: ${r.temperature ?? "-"} °C</div>
                    <div>Humidity: ${r.humidity ?? "-"}%</div>
                    <div>Flood Predicted: ${r.flood_prediction === 1 ? "YES" : "NO"}</div>
                    <div>Flood Prob: ${r.probability !== null ? (Number(r.probability).toFixed(1) + "%") : "-"}</div>
                </div><hr/>`;
        });
        html += `</div>`;
        resultsDiv.innerHTML = html;
    } catch (err) {
        console.error(err);
        resultsDiv.textContent = "Error getting prediction. Open DevTools Console for details.";
    }
});
// ...existing code...

