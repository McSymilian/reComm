#pragma once
#include <stdexcept>

class cannot_leave_group_as_last_member_error final : public std::runtime_error {
public:
    cannot_leave_group_as_last_member_error() : std::runtime_error("Cannot leave group - you are the last member. Delete the group instead") {}
};

