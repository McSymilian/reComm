#pragma once

#include <stdexcept>

class unknown_method_error final : public std::runtime_error {
public:
    explicit unknown_method_error(const std::string& method)
        : runtime_error("Unknown method: " + method) {
    }
};
