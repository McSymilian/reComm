#pragma once

#include <stdexcept>

class user_not_found_error final : public std::runtime_error {
public:
    explicit user_not_found_error()
        : runtime_error("User not found") {
    }
};