#pragma once

#include <stdexcept>

class unauthorized_error final : public std::runtime_error {
public:
    explicit unauthorized_error()
        : runtime_error("Unauthorized") {
    }
};