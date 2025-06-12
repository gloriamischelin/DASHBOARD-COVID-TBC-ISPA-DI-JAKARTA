import folium
from IPython.display import display, clear_output
import ipywidgets as widgets

# Sample data for COVID-19 with gender breakdown
data_covid = [
    {"lokasi": "Jakarta Selatan", "lat": -6.260, "lng": 106.794, "kasus": 12500, "meninggal": 500, "sembuh": 11000, "laki": 7000, "perempuan": 5500},
    {"lokasi": "Jakarta Timur", "lat": -6.215, "lng": 106.878, "kasus": 10700, "meninggal": 420, "sembuh": 9000, "laki": 6000, "perempuan": 4700},
    {"lokasi": "Jakarta Barat", "lat": -6.174, "lng": 106.799, "kasus": 9800, "meninggal": 380, "sembuh": 8500, "laki": 5200, "perempuan": 4600},
    {"lokasi": "Jakarta Utara", "lat": -6.123, "lng": 106.865, "kasus": 6700, "meninggal": 200, "sembuh": 6000, "laki": 3500, "perempuan": 3200},
    {"lokasi": "Jakarta Pusat", "lat": -6.175, "lng": 106.827, "kasus": 5400, "meninggal": 150, "sembuh": 5000, "laki": 2800, "perempuan": 2600}
]

# Sample data for TBC with gender breakdown
data_tbc = [
    {"lokasi": "Jakarta Selatan", "lat": -6.260, "lng": 106.794, "kasus": 3000, "meninggal": 100, "sembuh": 2900, "laki": 1800, "perempuan": 1200},
    {"lokasi": "Jakarta Timur", "lat": -6.215, "lng": 106.878, "kasus": 2500, "meninggal": 80, "sembuh": 2400, "laki": 1500, "perempuan": 1000},
    {"lokasi": "Jakarta Barat", "lat": -6.174, "lng": 106.799, "kasus": 2000, "meninggal": 60, "sembuh": 1900, "laki": 1200, "perempuan": 800},
    {"lokasi": "Jakarta Utara", "lat": -6.123, "lng": 106.865, "kasus": 1500, "meninggal": 40, "sembuh": 1400, "laki": 800, "perempuan": 700},
    {"lokasi": "Jakarta Pusat", "lat": -6.175, "lng": 106.827, "kasus": 1200, "meninggal": 30, "sembuh": 1150, "laki": 650, "perempuan": 550}
]

# Sample data for ISPA with gender breakdown
data_ispa = [
    {"lokasi": "Jakarta Selatan", "lat": -6.260, "lng": 106.794, "kasus": 4000, "meninggal": 50, "sembuh": 3800, "laki": 2200, "perempuan": 1800},
    {"lokasi": "Jakarta Timur", "lat": -6.215, "lng": 106.878, "kasus": 3500, "meninggal": 40, "sembuh": 3400, "laki": 1900, "perempuan": 1600},
    {"lokasi": "Jakarta Barat", "lat": -6.174, "lng": 106.799, "kasus": 3000, "meninggal": 30, "sembuh": 2900, "laki": 1600, "perempuan": 1400},
    {"lokasi": "Jakarta Utara", "lat": -6.123, "lng": 106.865, "kasus": 2500, "meninggal": 20, "sembuh": 2400, "laki": 1300, "perempuan": 1200},
    {"lokasi": "Jakarta Pusat", "lat": -6.175, "lng": 106.827, "kasus": 2200, "meninggal": 15, "sembuh": 2100, "laki": 1150, "perempuan": 1050}
]

def warna_lingkaran_covid(kasus):
    if kasus > 11000:
        return '#b22222'  # Firebrick
    elif kasus > 8000:
        return '#ff6347'  # Tomato
    else:
        return '#ffa07a'  # Light Salmon

def warna_lingkaran_tbc(kasus):
    if kasus > 2500:
        return '#00008b'  # Dark Blue
    elif kasus > 1500:
        return '#1e90ff'  # Dodger Blue
    else:
        return '#87cefa'  # Light Sky Blue

def warna_lingkaran_ispa(kasus):
    if kasus > 3500:
        return '#006400'  # Dark Green
    elif kasus > 2500:
        return '#228b22'  # Forest Green
    else:
        return '#7cfc00'  # Lawn Green

def create_map(selected_disease):
    # Use colorful OpenStreetMap tiles for a colorful base map
    m = folium.Map(location=[-6.2088, 106.8456], zoom_start=11, tiles='OpenStreetMap')

    if selected_disease == "COVID-19":
        data = data_covid
        color_func = warna_lingkaran_covid
        radius = 12
        title = "PENYEBARAN COVID-19"
    elif selected_disease == "TBC":
        data = data_tbc
        color_func = warna_lingkaran_tbc
        radius = 10
        title = "PENYEBARAN TBC"
    else:  # ISPA
        data = data_ispa
        color_func = warna_lingkaran_ispa
        radius = 10
        title = "PENYEBARAN ISPA"

    # Title marker on map (decorative)
    folium.map.Marker(
        [-6.38, 106.82],
        icon=folium.DivIcon(
            html=f'<div style="font-size:24pt; font-weight:700; color:#111827;">{title}</div>'
        )
    ).add_to(m)

    # Add CircleMarkers with color coding and popups
    for d in data:
        popup_html = f"""
        <div style="font-family: 'Inter', Arial, sans-serif; width: 260px; color: #374151;">
          <h4 style="margin-bottom:8px; color: #2563eb;">{d['lokasi']}</h4>
          <div style="font-size: 14px; margin-bottom: 5px;">
            <strong style="color:#ef4444;">Kasus:</strong> {d['kasus']}<br>
            <strong style="color:#10b981;">Sembuh:</strong> {d['sembuh']}<br>
            <strong style="color:#6b7280;">Meninggal:</strong> {d['meninggal']}<br>
            <hr style="margin:5px 0; border-color:#d1d5db;">
            <strong style="color:#3b82f6;">Laki-laki:</strong> {d['laki']}<br>
            <strong style="color:#ec4899;">Perempuan:</strong> {d['perempuan']}
          </div>
        </div>
        """
        folium.CircleMarker(
            location=[d['lat'], d['lng']],
            radius=radius,
            color=color_func(d['kasus']),
            weight=2,
            fill=True,
            fill_color=color_func(d['kasus']),
            fill_opacity=0.75,
            popup=folium.Popup(popup_html, max_width=280),
            tooltip=d['lokasi'],
        ).add_to(m)

    # Legend block with subtle styling
    legend_html = f'''
     <div style="
     position: fixed;
     bottom: 50px; left: 50px; width: 190px; height: 140px;
     background: white;
     border:2px solid #d1d5db; border-radius:12px;
     box-shadow: 0 6px 12px rgba(0,0,0,0.1);
     font-family: 'Inter', Arial, sans-serif;
     padding: 12px;
     font-size: 14px;
     color: #4b5563;
     z-index:9999;
     ">
     <b>Legenda {title}</b><br>
     <i style="background:{color_func(0)};width:18px;height:18px;float:left;margin-right:8px;opacity:0.85; border-radius:6px;"></i> Rendah<br><br>
     <i style="background:{color_func(9999)};width:18px;height:18px;float:left;margin-right:8px;opacity:0.85; border-radius:6px;"></i> Sedang<br><br>
     <i style="background:{color_func(99999)};width:18px;height:18px;float:left;margin-right:8px;opacity:0.85; border-radius:6px;"></i> Tinggi<br>
     </div>
     '''
    m.get_root().html.add_child(folium.Element(legend_html))

    return m

# Create dropdown widget for disease selection
dropdown = widgets.Dropdown(
    options=["COVID-19", "TBC", "ISPA"],
    value="COVID-19",
    description="Pilih Penyakit:",
    disabled=False,
    style={'description_width': 'initial'},
    layout=widgets.Layout(width='250px')
)

output = widgets.Output()

def on_change(change):
    if change['type'] == 'change' and change['name'] == 'value':
        with output:
            clear_output(wait=True)
            m = create_map(change['new'])
            display(m)

dropdown.observe(on_change)

# Display UI
display(dropdown)
with output:
    display(create_map(dropdown.value))
display(output)