#pragma once

#include <stdexcept>

class bad_request_format_error final : public std::runtime_error {
public:
    explicit bad_request_format_error()
        : runtime_error("Request should be in valid JSON format") {
    }
};
