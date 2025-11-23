#pragma once

#include <stdexcept>

class not_group_member_error final : public std::runtime_error {
public:
    explicit not_group_member_error()
        : runtime_error("Scoped user is not a member of the group") {
    }
};