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
from cherab.solps.plot import create_quadrangle_polycollection, create_triangle_polycollection, format_matplotlib_axes


plt.rcParams['figure.figsize'] = [5, 10]  # default figure size

# Load the simulation.
demos_directory = os.path.dirname(os.path.dirname(__file__))
simulation_directory = os.path.join(demos_directory, 'data', 'raw')
print('Loading simulation...')
sim = load_solps_from_raw_output(simulation_directory)
mesh = sim.mesh

# plot quadrangle and triangle meshes
# plot the quadrangle b2 mesh
collection_qm = create_quadrangle_polycollection(mesh, facecolor="none", edgecolor='b', linewidth=0.2)

fig_qmesh = plt.figure()
ax_qmesh = plt.subplot(111)
ax_qmesh.set_title("Quadrangle B2 Mesh")
ax_qmesh.add_collection(collection_qm)
format_matplotlib_axes(ax_qmesh, mesh)

#plot the quadrangle b2 mesh with b2 ion temperature values
collection_qti = create_quadrangle_polycollection(mesh, solps_data=sim.ion_temperature)
fig_qti = plt.figure()
ax_qti = plt.subplot(111)
ax_qti.set_title("B2 Ion Temperature")
ax_qti.add_collection(collection_qti)
cax_qti = ax_qti.inset_axes([1.05, 0, 0.05, 1])
fig_qti.colorbar(collection_qti, cax=cax_qti, label="Ion Temperature [eV]")
format_matplotlib_axes(ax_qti, mesh)

# plot the triangle B2 mesh
collection_tm = create_triangle_polycollection(mesh, facecolor="none", edgecolor='g', linewidth=0.25)

fig_tmesh = plt.figure()
ax_tmesh = plt.subplot(111)
ax_tmesh.set_title("Cherab Triangle Mesh")
ax_tmesh.add_collection(collection_tm)
format_matplotlib_axes(ax_tmesh, mesh)

# plot the triangle B2 mesh with b2 ion temperature values
collection_tti = create_triangle_polycollection(mesh, solps_data=sim.ion_temperature, edgecolors='face')

fig_tti = plt.figure()
ax_tti = plt.subplot(111)
ax_tti.set_title("Cherab Triangle mesh with Ion Temperature")
ax_tti.add_collection(collection_tti)
cax_tti = ax_tti.inset_axes([1.05, 0, 0.05, 1])
fig_tti.colorbar(collection_tti, cax=cax_tti, label="Ion Temperature [eV]")
format_matplotlib_axes(ax_tti, mesh)

plt.show()
