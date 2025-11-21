#pragma once

#include <stdexcept>

class friendship_request_already_sent_error final : public std::runtime_error {
public:
    explicit friendship_request_already_sent_error()
        : runtime_error("Friendship request has already been sent") {
    }
};