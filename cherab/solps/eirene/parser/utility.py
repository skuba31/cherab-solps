# Copyright 2016-2018 Euratom
# Copyright 2016-2018 United Kingdom Atomic Energy Authority
# Copyright 2016-2018 Centro de Investigaciones Energéticas, Medioambientales y Tecnológicas
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

import numpy as np


def read_block44(file_handle, ns, nx, ny):
    """ Read standard block in EIRENE code output file 'fort.44'

    :param file_handle: A python core file handle object as a result of a
      call to open('./fort.44').
    :param int ns: total number of species
    :param int nx: number of grid poloidal cells
    :param int ny: number of grid radial cells
    :return: ndarray of data with shape [ns, ny, nx]
    """
    data = []
    npoints = ns * nx * ny
    while len(data) < npoints:
        line = file_handle.readline().split()
        if line[0] == "*eirene":
            # This is a comment line. Ignore
            continue
        data.extend(line)
    data = np.asarray(data, dtype=float).reshape((ns, ny, nx))
    return data
