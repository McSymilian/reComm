#pragma once

#include <stdexcept>

class group_not_found_error final : public std::runtime_error {
public:
    explicit group_not_found_error()
        : runtime_error("Searched group not found") {
    }
};