#pragma once
#include "Friendship.h"
#include <vector>
#include <optional>

class FriendshipRepository {
public:
    virtual ~FriendshipRepository() = default;
    
    virtual bool save(const Friendship& friendship) = 0;
    virtual bool updateStatus(const UUIDv4::UUID& requesterId, 
                             const UUIDv4::UUID& addresseeId, 
                             FriendshipStatus status) = 0;
    virtual std::optional<Friendship> find(const UUIDv4::UUID& requesterId,
                                          const UUIDv4::UUID& addresseeId) = 0;
    virtual std::vector<UUIDv4::UUID> getFriends(const UUIDv4::UUID& userId) = 0;
    virtual std::vector<Friendship> getPendingRequests(const UUIDv4::UUID& userId) = 0;
    virtual bool areFriends(const UUIDv4::UUID& user1, const UUIDv4::UUID& user2) = 0;
};
