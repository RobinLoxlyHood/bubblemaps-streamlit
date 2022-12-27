import pandas as pd
import numpy as np
import streamlit as st
import folium
import seaborn as sns
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
from streamlit_folium import folium_static
import geopandas as gpd
import plotly.graph_objects as go
import leafmap.foliumap as leafmap


APP_TITLE = 'Visualisasi Data POI'
def filters_desa(df_jkt):
    filters_desa_list = ['ALL']+list(df_jkt['nama_desa'].unique())
    filters_desa_list.sort()
    filters_desa = st.sidebar.selectbox('Pilih Desa :', filters_desa_list)
    return filters_desa

# def multiselect_kategori_filters(df_jkt):
#     kategori_list = ['Belum Memilih']+list(df_jkt['nama_kategori'].unique())
#     kategori_list.sort()
#     selectbox = st.sidebar.multiselect('Pilih Kategori POI :', kategori_list)
#     return selectbox
def radiobox_pilih_kategori():
    radio= st.sidebar.radio(
        "Pilih Value",
        ('Jumlah Kategori POI', 'Jumlah Penduduk'))
    return radio

# def display_map(df_jkt, kategori, selectbox):
#     map = folium.Map(location=[-6.2, 106.90], zoom_start=11, scrollWhileZoom=False, tiles='cartodbdark_matter')

#     # choropleth = folium.Choropleth(
#     #     geo_data='demografi_jakarta_utara.geojson',
#     #     data=df_jkt,
#     #     columns=('nama_desa', 'JUMLAH_PEN'),
#     #     key_on='feature.properties.nama_desa',
#     #     fill_color='YlOrRd',
#     #     line_opacity=0.8,
#     #     legend_name='nama_desa',
#     #     highlight=True
#     # )
#     # choropleth.geojson.add_to(map)
#     #Loop through each row in the dataframe

#     selectbox=selectbox
#     df_jkt = df_jkt.query("nama_kategori in @selectbox")
#     for _, r in df_jkt.iterrows():
        
#         # Without simplifying the representation of each borough,
#         # the map might not be displayed
#         sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
#         geo_j = sim_geo.to_json()
#         geo_j = folium.GeoJson(data=geo_j)
#         #folium.Popup(r['nama_kategori']).add_to(geo_j)
#         folium.Popup(r['nama_merchant']).add_to(geo_j)
#         # folium.Marker(icon = folium.Icon(color='red'))
#         geo_j.add_to(map)

#     #selectbox=st.write(selectbox)
#     st_map=st_folium(map, width=700, height=450)
#     return st_map

# def display_map(df_poi,selectbox):
#     map=leafmap.Map(center=[-6.2, 106.90], zoom=11)
#     df_jkt='demografi_jakarta_utara.geojson'
#     selectbox=selectbox
#     df_poi= df_poi.query("nama_kategori in @selectbox")
#     map.add_geojson(df_jkt, layer_name='POI Jakarta Utara')
#     map.add_circle_markers_from_xy(
#         df_poi,
#         x="lon_centroid",
#         y="lat_centroid",
#         radius=10,
#         color="blue", 
#         fill_color="blue"
#     )
#     map.to_streamlit(width=700, height=500)


#Legend
def add_categorical_legend(folium_map, title, colors, labels):
    if len(colors) != len(labels):
        raise ValueError("colors and labels must have the same length.")

    color_by_label = dict(zip(labels, colors))
    
    legend_categories = ""     
    for label, color in color_by_label.items():
        legend_categories += f"<li><span style='background:{color}'></span>{label}</li>"
        
    legend_html = f"""
    <div id='maplegend' class='maplegend'>
      <div class='legend-title'>{title}</div>
      <div class='legend-scale'>
        <ul class='legend-labels'>
        {legend_categories}
        </ul>
      </div>
    </div>
    """
    script = f"""
        <script type="text/javascript">
        var oneTimeExecution = (function() {{
                    var executed = false;
                    return function() {{
                        if (!executed) {{
                             var checkExist = setInterval(function() {{
                                       if ((document.getElementsByClassName('leaflet-top leaflet-right').length) || (!executed)) {{
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.display = "flex"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.flexDirection = "column"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].innerHTML += `{legend_html}`;
                                          clearInterval(checkExist);
                                          executed = true;
                                       }}
                                    }}, 100);
                        }}
                    }};
                }})();
        oneTimeExecution()
        </script>
      """
   

    css = """
    <style type='text/css'>
      .maplegend {
        z-index:9999;
        float:right;
        background-color: rgba(255, 255, 255, 1);
        border-radius: 5px;
        border: 2px solid #bbb;
        padding: 10px;
        font-size:12px;
        positon: relative;
      }
      .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
      .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
      .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
      .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 0px solid #ccc;
        }
      .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
      .maplegend a {
        color: #777;
        }
    </style>
    """

    folium_map.get_root().header.add_child(folium.Element(script + css))

    return folium_map

def display_bubble_map_all(df_poi, radio):
    n = folium.Map(location=[-6.2, 106.90], zoom_start=11, scrollWhileZoom=False, tiles='cartodbdark_matter')
    radio=radio
    if radio=='Jumlah Kategori POI':
        df_poi=df_poi.copy()
        jumlah_poi=[]
        for i in df_poi.nama_desa:
            nama_desa=df_poi[(df_poi['nama_desa'] == i)]
            jumlah_poi.append(len(nama_desa.gid))
        df_poi['jumlah_poi']=jumlah_poi

        #Pembagian minimal value radius
        x1=max(jumlah_poi)-1
        x2=int(x1/2)
        radius=[]
        color_radius=[]
        for i in df_poi.jumlah_poi:
            if i > x1:
                radius.append(15)
                color_radius.append('red')
            elif i > x2:
                radius.append(10)
                color_radius.append('yellow')
            else:
                radius.append(5)
                color_radius.append('blue')
        df_poi['radius']=radius
        df_poi['color_radius']=color_radius
        data=df_poi.copy()
        for row in data.iterrows():
            row_values = row[1]
            location = [row_values['lat_centroid'], row_values['lon_centroid']]
            popup = (row_values['nama_desa'])
            color=(row_values['color_radius'])
            radius=(row_values['radius'])

            marker = folium.CircleMarker(location = location,popup=popup,color='black', fill_color=color, radius=radius)
            marker.add_to(n)
    
        legend_map = add_categorical_legend(n,'Legend',
                                            colors = ['green', 'blue', 'yellow', 'red'],
                                            labels = ['Sangat Sedikit', 'Sedikit', 'Normal', 'Banyak']
                                            )
        fs=folium_static(legend_map, width = 700, height = 500)  
    else:
        df_poi=df_poi.copy()
        #Pembagian minimal value radius
        x1=int(df_poi.JUMLAH_PEN.max())-1
        x2=int(x1/2)
        radius=[]
        color_radius=[]
        for i in df_poi.JUMLAH_PEN:
            if i > x1:
                radius.append(15)
                color_radius.append('red')
            elif i > x2:
                radius.append(10)
                color_radius.append('yellow')
            else:
                radius.append(5)
                color_radius.append('blue')
        df_poi['radius_jumlah_pen']=radius
        df_poi['color_radius_jumlah_pen']=color_radius
        data=df_poi.copy()
        for row in data.iterrows():
            row_values = row[1]
            location = [row_values['lat_centroid'], row_values['lon_centroid']]
            popup = (row_values['nama_desa'])
            color=(row_values['color_radius_jumlah_pen'])
            radius=(row_values['radius_jumlah_pen'])

            marker = folium.CircleMarker(location = location,popup=popup,color='black', fill_color=color, radius=radius)
            marker.add_to(n)
    
        legend_map = add_categorical_legend(n,'Legend',
                                            colors = ['green', 'blue', 'yellow', 'red'],
                                            labels = ['Sangat Sedikit', 'Sedikit', 'Normal', 'Banyak']
                                            )
        fs=folium_static(legend_map, width = 700, height = 500)
    return fs    
    # else:
    #     radio=radio
    #     if radio=='Jumlah Kategori POI':
    #         df_poi= df_poi[(df_poi['nama_desa'] == selectbox)]
    #         # jumlah_poi=[]
    #         # for i in df_poi.nama_desa:
    #         #     nama_desa=df_poi[(df_poi['nama_desa'] == i)]
    #         #     jumlah_poi.append(len(nama_desa.gid))
    #         # df_poi['jumlah_poi']=jumlah_poi

    #         #Pembagian minimal value radius
    #         x1=int(df_poi.jumlah_poi.max())
    #         x2=int(x1/2)
    #         x3=int(x2/2)
    #         radius=[]
    #         color_radius=[]
    #         for i in df_poi.jumlah_poi:
    #             if i < x3:
    #                 radius.append(5)
    #                 color_radius.append('blue')
    #             elif i < x2:
    #                 radius.append(10)
    #                 color_radius.append('yellow')
    #             elif i < x1:
    #                 radius.append(15)
    #                 color_radius.append('red')
    #             else:
    #                 radius.append(3)
    #                 color_radius.append('green')
    #         df_poi['radius']=radius
    #         df_poi['color_radius']=color_radius
    #         data=df_poi.copy()
    #         for row in data.iterrows():
    #             row_values = row[1]
    #             location = [row_values['lat_centroid'], row_values['lon_centroid']]
    #             popup = (row_values['nama_merchant'])
    #             color=(row_values['color_radius'])
    #             radius=(row_values['radius'])

    #             marker = folium.CircleMarker(location = location,popup=popup,color='black', fill_color=color, radius=radius)
    #             marker.add_to(n)
    
    #         legend_map = add_categorical_legend(n,'Legend',
    #                                         colors = ['green', 'blue', 'yellow', 'red'],
    #                                         labels = ['Sangat Sedikit', 'Sedikit', 'Normal', 'Banyak']
    #                                         )
    #         fs=folium_static(legend_map, width = 700, height = 500)
    #     else:
    #         df_poi=df_poi.query("nama_desa in @selectbox")
    #         #Pembagian minimal value radius
    #         x1=int(df_poi.JUMLAH_PEN.max())
    #         x2=int(x1/2)
    #         x3=int(x2/2)
    #         radius=[]
    #         color_radius=[]
    #         for i in df_poi.JUMLAH_PEN:
    #             if i < x3:
    #                 radius.append(5)
    #                 color_radius.append('blue')
    #             elif i < x2:
    #                 radius.append(10)
    #                 color_radius.append('yellow')
    #             elif i < x1:
    #                 radius.append(15)
    #                 color_radius.append('red')
    #             else:
    #                 radius.append(3)
    #                 color_radius.append('green')
    #         df_poi['radius_jumlah_pen']=radius
    #         df_poi['color_radius_jumlah_pen']=color_radius
    #         data=df_poi.copy()
    #         for row in data.iterrows():
    #             row_values = row[1]
    #             location = [row_values['lat_centroid'], row_values['lon_centroid']]
    #             popup = (row_values['nama_desa'])
    #             color=(row_values['color_radius_jumlah_pen'])
    #             radius=(row_values['radius_jumlah_pen'])

    #             marker = folium.CircleMarker(location = location,popup=popup,color='black', fill_color=color, radius=radius)
    #             marker.add_to(n)
    
    #         legend_map = add_categorical_legend(n,'Legend',
    #                                         colors = ['green', 'blue', 'yellow', 'red'],
    #                                         labels = ['Sangat Sedikit', 'Sedikit', 'Normal', 'Banyak']
    #                                         )
    #         fs=folium_static(legend_map, width = 700, height = 500)
    # return fs

#addcolor colom
def categorycolors(counter):
    if counter['nama_kategori'] == 'Law & Defend':
        return 'green'
    elif counter['nama_kategori'] == 'Transportation and Logistic':
        return 'blue'
    elif counter['nama_kategori'] == 'Entertainment':
        return 'red'
    elif counter['nama_kategori'] == 'Market':
        return 'purple'
    elif counter['nama_kategori'] == 'Education':
        return 'orange'
    elif counter['nama_kategori'] == 'Property':
        return 'darkred'
    elif counter['nama_kategori'] == 'Social Economy':
        return 'lightred'
    elif counter['nama_kategori'] == 'Sport':
        return 'beige'
    elif counter['nama_kategori'] == 'Tourism':
        return 'darkblue'
    elif counter['nama_kategori'] == 'Medical':
        return 'darkgreen'
    elif counter['nama_kategori'] == 'Commercial':
        return 'cadetblue'
    else:
        return 'gray'

def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)

    #load_data
    df_poi = pd.read_csv('poi.csv')
    df_desa= pd.read_csv('demografi_jakarta_utara.csv')

    df_jkt = gpd.read_file('demografi_jakarta_utara.geojson')
    geoPOI=gpd.read_file('poi.geojson')

    #Join
    geoPOI.crs = df_jkt.crs
    #join_left_df = geoPOI.sjoin(df_jkt, how="left")
    join_right_df= geoPOI.sjoin(df_jkt, how="right")

    #addcolor
    join_right_df['color']=join_right_df.apply(categorycolors, axis=1)
    join_right_df = join_right_df.to_crs(4326)
    join_right_df['lon_centroid'] = join_right_df.centroid.x  
    join_right_df['lat_centroid'] = join_right_df.centroid.y
    jumlah_poi=[]
    for i in join_right_df.nama_desa:
        nama_desa=join_right_df[(join_right_df['nama_desa'] == i)]
        jumlah_poi.append(len(nama_desa.gid))
    join_right_df['jumlah_poi']=jumlah_poi


    # Display Visual and maps
    #maps
    #kategori = display_kategori_filters(df_jkt=join_left_df)
    #selectbox= multiselect_kategori_filters(df_jkt=join_left_df)
    #desa=filters_desa(df_jkt=join_right_df)
    #selectbox= multiselect_kategori_filters(df_jkt=join_right_df)
    radio = radiobox_pilih_kategori()
    display_bubble_map_all(df_poi=join_right_df, radio=radio)

    #display_map(df_jkt=join_left_df, kategori=kategori, selectbox=selectbox)
    

if __name__ == "__main__":
    main()