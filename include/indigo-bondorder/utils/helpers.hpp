/** @file helpers.hpp
 *  @brief Construction helper function declarations
 *  @author Ivan Welsh
 *  @date 8 January 2018
 *  @lastmodify 8 January 2018
 *  @version 0.1
 *  @copyright The MIT License
 */
#include "../api.hpp"

#ifndef INDIGO_BONDORDER_UTILS_HELPERS_HPP
#define INDIGO_BONDORDER_UTILS_HELPERS_HPP

namespace indigo_bondorder {
  /// @brief Helper function to generate a new Atom instance.
  Atom_p CreateAtom();
  
  /// @brief Helper function to generate a new Bond instance.
  Bond_p CreateBond();
  
  /// @brief Helper function to generate a new Molecule instance.
  Molecule_p CreateMolecule();
  
}

#endif /* INDIGO_BONDORDER_UTILS_HELPERS_HPP */
