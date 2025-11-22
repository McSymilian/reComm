#pragma once

#include <stdexcept>
#include <string>

class missing_required_field_error final : public std::runtime_error {
public:
    explicit missing_required_field_error(const std::string& fieldName)
        : runtime_error("Missing required field: " + fieldName) {
    }
};

