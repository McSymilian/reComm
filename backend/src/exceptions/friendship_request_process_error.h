#pragma once

#include <stdexcept>

class friendship_request_process_error final : public std::runtime_error {
public:
    explicit friendship_request_process_error()
        : runtime_error("Error occurred while processing friendship request") {
    }
};