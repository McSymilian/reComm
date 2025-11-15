#pragma once

#include <stdexcept>

class user_already_exists_error final : public std::runtime_error {
public:
    explicit user_already_exists_error(const std::string& method)
        : runtime_error("Unknown method: " + method) {
    }
};
