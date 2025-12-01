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

// Button click for future backend integration
document.getElementById("checkFlood").addEventListener("click", () => {
    const province = provinceSelect.value;
    const city = citySelect.value;
    const district = districtSelect.value;
    const subdistrict = subdistrictSelect.value;

    if (!province || !city || !district || !subdistrict) {
        resultsDiv.textContent = "Please select all fields!";
        return;
    }

    resultsDiv.textContent = `Selected: ${province} / ${city} / ${district} / ${subdistrict}`;
    // Here, you can call your backend API to get prediction
});
