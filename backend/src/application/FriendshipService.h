#pragma once
#include "../domain/friendship/FriendshipRepository.h"
#include "../domain/user/UserRepository.h"
#include "../exceptions/user_not_found_error.h"
#include <memory>

#include "../exceptions/already_friends_error.h"
#include "../exceptions/cannot_be_self_friend_error.h"
#include "../exceptions/friendship_request_already_sent_error.h"
#include "../exceptions/friendship_request_already_processed_error.h"
#include "../exceptions/friendship_request_not_found_error.h"
#include "../exceptions/friendship_request_process_error.h"
#include "../exceptions/save_friendship_request_error.h"

enum class FriendRequestResult {
    SUCCESS,
    ALREADY_FRIENDS,
    ALREADY_PENDING,
    USER_NOT_FOUND,
    CANNOT_ADD_YOURSELF
};

enum class AcceptRequestResult {
    SUCCESS,
    REQUEST_NOT_FOUND,
    ALREADY_PROCESSED
};

class FriendshipService {
    std::shared_ptr<FriendshipRepository> friendshipRepo;
    std::shared_ptr<UserRepository> userRepo;

public:
    FriendshipService(std::shared_ptr<FriendshipRepository> fRepo,
                     std::shared_ptr<UserRepository> uRepo)
        : friendshipRepo(std::move(fRepo)), userRepo(std::move(uRepo)) {}

    void sendFriendRequest(
        const UUIDv4::UUID& requesterId,
        const std::string& addresseeUsername
    ) const {
        if(!userRepo->exists(requesterId))
            throw user_not_found_error();

        const auto addressee = userRepo->findByUsername(addresseeUsername);
        if(!addressee.has_value())
            throw user_not_found_error();

        if(requesterId == addressee->uuid)
           throw cannot_be_self_friend_error();

        if(friendshipRepo->areFriends(requesterId, addressee->uuid))
            throw already_friends_error();

        if(friendshipRepo->find(requesterId, addressee->uuid))
            throw friendship_request_already_sent_error();

        if (friendshipRepo->find(addressee->uuid, requesterId))
            return acceptFriendRequest(requesterId, addressee->uuid);

        const auto now = std::chrono::system_clock::now();
        const Friendship friendship{
            requesterId,
            addressee->uuid,
            FriendshipStatus::PENDING,
            now,
            now
        };

        if (!friendshipRepo->save(friendship))
            throw save_friendship_request_error();
    }

    void acceptFriendRequest(const UUIDv4::UUID& userId,
                                           const UUIDv4::UUID& requesterId) const {
        const auto friendship = friendshipRepo->find(requesterId, userId);
        if(!friendship)
            throw friendship_request_not_found_error();

        if(friendship->status != FriendshipStatus::PENDING)
           throw friendship_request_already_processed_error();

        if (!friendshipRepo->updateStatus(requesterId, userId, FriendshipStatus::ACCEPTED))
            throw friendship_request_process_error();
    }

    void rejectFriendRequest(
        const UUIDv4::UUID& userId,
        const UUIDv4::UUID& requesterId
    ) const {
        const auto friendship = friendshipRepo->find(requesterId, userId);
        if(!friendship)
            throw friendship_request_not_found_error();

        if(friendship->status != FriendshipStatus::PENDING)
            throw friendship_request_already_processed_error();

        if (!friendshipRepo->updateStatus(requesterId, userId, FriendshipStatus::REJECTED))
            throw friendship_request_process_error();
    }

    std::vector<UUIDv4::UUID> getFriends(const UUIDv4::UUID& userId) const {
        return friendshipRepo->getFriends(userId);
    }

    std::vector<Friendship> getPendingRequests(const UUIDv4::UUID& userId) const {
        return friendshipRepo->getPendingRequests(userId);
    }
};
