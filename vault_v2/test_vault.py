import openmc
import vault
import numpy as np
import matplotlib.pyplot as plt

point = openmc.stats.Point((1800, 400, 100))
src = openmc.IndependentSource(space=point)
src.energy = openmc.stats.Discrete([14.1E6], [1.0])
src.strength = 1.0

settings = openmc.Settings()
settings.run_mode = 'fixed source'
settings.source = src
settings.batches = 100
settings.inactive = 0
settings.particles = int(1e5)

water = openmc.Material(name='water')
water.add_element('O', 1/3)
water.add_element('H', 2/3)
water.set_density('g/cc', 1.0)

water_sphere = openmc.Sphere(r=100, 
                             x0=src.space.xyz[0]+100,
                             y0=src.space.xyz[1],
                             z0=src.space.xyz[2])
water_cell = openmc.Cell(region=-water_sphere, fill=water)
overall_exclusion_region = -water_sphere

tally = openmc.Tally()
tally.filters = [openmc.CellFilter(water_cell)]
tally.scores = ['flux']
tallies = openmc.Tallies([tally])

model = vault.build_vault_model(settings=settings,
                                tallies=tallies,
                                added_cells=[water_cell],
                                added_materials=[water],
                                overall_exclusion_region=overall_exclusion_region)

model.geometry.export_to_xml()
model.settings.export_to_xml()
model.materials.export_to_xml()

plot = openmc.Plot()
plot.filename = 'yz'
plot.basis = 'yz'
plot.origin = (1800, 400, 100)
plot.width = (10000, 10000)  
plot.pixels = (1000, 1000)  
plot.color_by = 'cell'  
plots = openmc.Plots([plot])
plots.export_to_xml()

# Esegui il comando per generare il plot
openmc.plot_geometry()

# Usa Matplotlib per mostrare l'immagine generata
img = plt.imread('yz.png')
plt.imshow(img)
plt.axis('on')  # Opzionale, per nascondere gli assi
plt.show()

# vox_plot = openmc.Plot()
# vox_plot.type = 'voxel'
# vox_plot.width = (100., 100., 50.)
# vox_plot.pixels = (400, 400, 200)
# vox_plot.color_by = 'material'  # o 'cell' se preferisci colorare per celle
# vox_plot.type = 'voxel'  # Imposta il tipo di plot come 'voxel'

# # Esporta il plot in formato VTK
# vtk_file_path = vox_plot.to_vtk(output='plot_output.vti')
# print(f"File VTK creato in: {vtk_file_path}")