# Copyright 2016-2021 Euratom
# Copyright 2016-2021 United Kingdom Atomic Energy Authority
# Copyright 2016-2021 Centro de Investigaciones Energéticas, Medioambientales y Tecnológicas
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

from raysect.core.math.function.float cimport Function3D
from cherab.core.atomic cimport Line
from cherab.core.plasma cimport PlasmaModel
from cherab.core.species cimport Species
from cherab.core.model.lineshape cimport LineShapeModel


cdef class SOLPSLineEmitter(PlasmaModel):

    cdef:
        Line _line
        double _wavelength
        Species _target_species
        LineShapeModel _lineshape
        Function3D _power_density
        
        object _lineshape_class, _lineshape_args, _lineshape_kwargs

    cdef int _populate_cache(self) except -1
