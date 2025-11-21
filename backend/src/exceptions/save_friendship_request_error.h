#pragma once

#include <stdexcept>

class save_friendship_request_error final : public std::runtime_error {
public:
    explicit save_friendship_request_error()
        : runtime_error("Unable to save friends request") {
    }
};