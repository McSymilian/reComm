#pragma once

#include <stdexcept>

class cannot_be_self_friend_error final : public std::runtime_error {
public:
    explicit cannot_be_self_friend_error()
        : runtime_error("Cannot add yourself as a friend") {
    }
};