(() => {
  const tileUrl = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
  const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors';

  const picker = document.getElementById("map-picker");
  if (picker && window.L) {
    const startLat = Number(picker.dataset.lat) || -9.6658;
    const startLng = Number(picker.dataset.lng) || -35.7353;
    const map = L.map(picker).setView([startLat, startLng], picker.dataset.lat ? 15 : 12);
    L.tileLayer(tileUrl, { maxZoom: 19, attribution }).addTo(map);
    let marker = null;
    const latField = document.getElementById("latitude");
    const lngField = document.getElementById("longitude");
    const setPoint = (lat, lng) => {
      latField.value = lat.toFixed(6);
      lngField.value = lng.toFixed(6);
      if (marker) marker.setLatLng([lat, lng]);
      else marker = L.marker([lat, lng]).addTo(map);
    };
    if (picker.dataset.lat && picker.dataset.lng) setPoint(startLat, startLng);
    map.on("click", (event) => setPoint(event.latlng.lat, event.latlng.lng));
    window.setTimeout(() => map.invalidateSize(), 100);
  }

  const publicMap = document.getElementById("public-map");
  if (publicMap && window.L) {
    const map = L.map(publicMap).setView([-9.6658, -35.7353], 8);
    L.tileLayer(tileUrl, { maxZoom: 19, attribution }).addTo(map);
    const bounds = [];
    document.querySelectorAll(".map-points [data-lat][data-lng]").forEach((point) => {
      const lat = Number(point.dataset.lat);
      const lng = Number(point.dataset.lng);
      if (!Number.isFinite(lat) || !Number.isFinite(lng)) return;
      const marker = L.marker([lat, lng]).addTo(map);
      const link = document.createElement("a");
      link.href = point.dataset.url;
      link.textContent = point.dataset.title;
      marker.bindPopup(link);
      bounds.push([lat, lng]);
    });
    if (bounds.length) map.fitBounds(bounds, { padding: [24, 24], maxZoom: 13 });
    window.setTimeout(() => map.invalidateSize(), 100);
  }

  const detailMap = document.getElementById("detail-map");
  if (detailMap && window.L) {
    const lat = Number(detailMap.dataset.lat);
    const lng = Number(detailMap.dataset.lng);
    const map = L.map(detailMap).setView([lat, lng], 15);
    L.tileLayer(tileUrl, { maxZoom: 19, attribution }).addTo(map);
    const title = document.createElement("span");
    title.textContent = detailMap.dataset.title;
    L.marker([lat, lng]).addTo(map).bindPopup(title).openPopup();
    window.setTimeout(() => map.invalidateSize(), 100);
  }
})();
