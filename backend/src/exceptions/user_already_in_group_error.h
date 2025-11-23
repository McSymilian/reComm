#pragma once
#include <stdexcept>

class user_already_in_group_error final : public std::runtime_error {
public:
    user_already_in_group_error() : std::runtime_error("User is already a member of this group") {}
};

