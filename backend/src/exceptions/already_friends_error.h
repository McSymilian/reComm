#pragma once

#include <stdexcept>

class already_friends_error final : public std::runtime_error {
public:
    explicit already_friends_error()
        : runtime_error("Accounts are already friends") {
    }
};