#pragma once

#include <stdexcept>

class invalid_credentials_error final : public std::runtime_error {
public:
    explicit invalid_credentials_error()
        : runtime_error("Invalid credentials provided") {
    }
};
