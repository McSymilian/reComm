#pragma once

#include <stdexcept>

class cannot_add_non_friend_to_group_error final : public std::runtime_error {
public:
    cannot_add_non_friend_to_group_error() : std::runtime_error("Cannot add user to group - user is not a friend") {}
};