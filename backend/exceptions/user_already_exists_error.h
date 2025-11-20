#pragma once

#include <stdexcept>

class user_already_exists_error final : public std::runtime_error {
public:
    explicit user_already_exists_error()
        : runtime_error("User already exists") {
    }
};
