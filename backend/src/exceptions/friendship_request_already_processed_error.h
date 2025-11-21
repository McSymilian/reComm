#pragma once

#include <stdexcept>

class friendship_request_already_processed_error final : public std::runtime_error {
public:
    explicit friendship_request_already_processed_error()
        : runtime_error("Friendship request has already been processed") {
    }
};