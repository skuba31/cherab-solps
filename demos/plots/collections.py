# Copyright 2014-2020 United Kingdom Atomic Energy Authority
#
# Licensed under the EUPL, Version 1.1 or – as soon they will be approved by the
# European Commission - subsequent versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at:
#
# https://joinup.ec.europa.eu/software/page/eupl5
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the Licence is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied.
#
# See the Licence for the specific language governing permissions and limitations
# under the Licence.
import os
import matplotlib.pyplot as plt

from cherab.solps import load_solps_from_raw_output


# Load the simulation.
demos_directory = os.path.dirname(os.path.dirname(__file__))
simulation_directory = os.path.join(demos_directory, 'data', 'raw')
print('Loading simulation...')
sim = load_solps_from_raw_output(simulation_directory)
mesh = sim.mesh

# plot quadrangle and triangle meshes
# plot the quadrangle b2 mesh
collection_qm = mesh.create_quadrangle_polycollection()

fig_qmesh = plt.figure(figsize=(10, 20))
ax_qmesh = plt.subplot(111)
ax_qmesh.set_title("Quadrangle B2 Mesh")
ax_qmesh.add_collection(collection_qm)
mesh.format_matplotlib_axes(ax_qmesh)

#plot the quadrangle b2 mesh with b2 ion temperature values
collection_qti = mesh.create_quadrangle_polycollection(solps_data=sim.ion_temperature)
fig_qti = plt.figure(figsize=(10, 20))
ax_qti = plt.subplot(111)
ax_qti.set_title("B2 Ion Temperature [eV]")
ax_qti.add_collection(collection_qti)
cax_qti = ax_qti.inset_axes([1.05, 0, 0.05, 1])
fig_qti.colorbar(collection_qti, cax=cax_qti, label="Ion Temperature [eV]")
mesh.format_matplotlib_axes(ax_qti)

# plot the triangle B2 mesh
collection_tm = mesh.create_triangle_polycollection()

fig_tmesh = plt.figure(figsize=(10, 20))
ax_tmesh = plt.subplot(111)
ax_tmesh.set_title("Triangle B2 Mesh")
ax_tmesh.add_collection(collection_tm)
mesh.format_matplotlib_axes(ax_tmesh)

# plot the triangle B2 mesh with b2 ion temperature values
collection_tti = mesh.create_triangle_polycollection(solps_data=sim.ion_temperature, edgecolors='face')

fig_tti = plt.figure(figsize=(10, 20))
ax_tti = plt.subplot(111)
ax_tti.set_title("B2 Ion Temperature [eV]")
ax_tti.add_collection(collection_tti)
cax_tti = ax_tti.inset_axes([1.05, 0, 0.05, 1])
fig_tti.colorbar(collection_tti, cax=cax_tti, label="Ion Temperature [eV]")
mesh.format_matplotlib_axes(ax_tti)

plt.show()
