#pragma once

#include <stdexcept>

class friendship_request_not_found_error final : public std::runtime_error {
public:
    explicit friendship_request_not_found_error()
        : runtime_error("Cannot find the specified friendship request") {
    }
};