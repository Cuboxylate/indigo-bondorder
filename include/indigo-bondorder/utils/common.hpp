/** @file common.hpp
 *  @brief Utility functions declarations.
 *  @author Ivan Welsh
 *  @date 21 August 2017
 *  @lastmodify 6 January 2018
 *  @version 0.1
 *  @copyright The MIT License
 */

#ifndef INDIGO_BONDORDER_UTILS_COMMON_HPP
#define INDIGO_BONDORDER_UTILS_COMMON_HPP

#include <algorithm>

#include "../api.hpp"

namespace indigo_bondorder {
  namespace utils {
    
    /// @brief Convert a string to upper case.
    String toUpper(const String*);
    
    /// @brief Convert a string to lower case.
    String toLower(const String*);
    
    /// @brief Convert a string to lower case with leading upper case.
    String toUpperFirst(const String*);
    
    /// @brief Generate a random string.
    String randomString(size_t);
    
  }  // namespace utils
}  // namespace indigo_bondorder


#endif /* INDIGO_BONDORDER_UTILS_COMMON_HPP */
