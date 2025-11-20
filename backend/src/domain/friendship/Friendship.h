#pragma once

#include <chrono>
#include "uuid_v4.h"

enum class FriendshipStatus {
    PENDING,
    ACCEPTED,
    REJECTED
};

struct Friendship {
    UUIDv4::UUID requesterId;
    UUIDv4::UUID addresseeId;
    FriendshipStatus status;
    std::chrono::system_clock::time_point createdAt;
    std::chrono::system_clock::time_point updatedAt;
};
