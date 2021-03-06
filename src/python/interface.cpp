//
//  python_interface.cpp
//  indigo-bondorder
//
//  Created by Ivan Welsh on 6/01/18.
//  Copyright © 2018 Hermes Productions. All rights reserved.
//

#include "api.hpp"
#include "python/interface.hpp"



namespace py = pybind11;

PYBIND11_MODULE(pyindigox, m) {
  using namespace indigo_bondorder;
  GenerateOptions(m);
  GeneratePyAtom(m);
  GeneratePyBond(m);
  GeneratePyElement(m);
  GeneratePyMolecule(m);
  GeneratePyPeriodicTable(m);
}


