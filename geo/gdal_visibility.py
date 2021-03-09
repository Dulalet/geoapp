import pyvisgraph as vg
import folium


polys = [[vg.Point(0.0,1.0), vg.Point(3.0,1.0), vg.Point(1.5,4.0)],
         [vg.Point(4.0,4.0), vg.Point(7.0,4.0), vg.Point(5.5,8.0)]]
graph = vg.VisGraph()
graph.build(polys)
# shortest = g.shortest_path(vg.Point(1.5,0.0), vg.Point(4.0, 6.0))
# print(shortest)

start_point = vg.Point(0.1, 0.1)
end_point = vg.Point(6.851959, 7.290270)

shortest_path = graph.shortest_path(start_point, end_point)

# Plot of the path using folium
geopath = [[point.y, point.x] for point in shortest_path]
geomap = folium.Map([0, 0], zoom_start=2)
for point in geopath:
    folium.Marker(point, popup=str(point)).add_to(geomap)
folium.PolyLine(geopath).add_to(geomap)

# Add a Mark on the start and positions in a different color
folium.Marker(geopath[0], popup=str(start_point), icon=folium.Icon(color='red')).add_to(geomap)
folium.Marker(geopath[-1], popup=str(end_point), icon=folium.Icon(color='red')).add_to(geomap)

# Save the interactive plot as a map
output_name = 'example_shortest_path_plot.html'
geomap.save(output_name)
print('Output saved to: {}'.format(output_name))

# https://github.com/jonnyhuck/Viewshed
