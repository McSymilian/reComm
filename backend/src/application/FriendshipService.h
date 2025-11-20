#pragma once
#include "../domain/friendship/FriendshipRepository.h"
#include "../domain/user/UserRepository.h"
#include <memory>

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

    FriendRequestResult sendFriendRequest(const UUIDv4::UUID& requesterId,
                                         const std::string& addresseeUsername) const {
        if(!userRepo->exists(requesterId))
            return FriendRequestResult::USER_NOT_FOUND;

        auto addressee = userRepo->findByUsername(addresseeUsername);
        //todo refactor to exception driven workflow
        if(!addressee.has_value())
            return FriendRequestResult::USER_NOT_FOUND;

        if(requesterId == addressee->uuid)
            return FriendRequestResult::CANNOT_ADD_YOURSELF;

        if(friendshipRepo->areFriends(requesterId, addressee->uuid))
            return FriendRequestResult::ALREADY_FRIENDS;

        if(friendshipRepo->find(requesterId, addressee->uuid))
            return FriendRequestResult::ALREADY_PENDING;
        //todo what if there is a pending request from the other side?

        const auto now = std::chrono::system_clock::now();
        Friendship friendship{
            requesterId,
            addressee->uuid,
            FriendshipStatus::PENDING,
            now,
            now
        };

        return friendshipRepo->save(friendship) 
            ? FriendRequestResult::SUCCESS 
            : FriendRequestResult::USER_NOT_FOUND;
    }

    AcceptRequestResult acceptFriendRequest(const UUIDv4::UUID& userId,
                                           const UUIDv4::UUID& requesterId) const {
        auto friendship = friendshipRepo->find(requesterId, userId);
        if(!friendship)
            return AcceptRequestResult::REQUEST_NOT_FOUND;

        if(friendship->status != FriendshipStatus::PENDING)
            return AcceptRequestResult::ALREADY_PROCESSED;

        return friendshipRepo->updateStatus(requesterId, userId, FriendshipStatus::ACCEPTED)
            ? AcceptRequestResult::SUCCESS
            : AcceptRequestResult::REQUEST_NOT_FOUND;
    }

    AcceptRequestResult rejectFriendRequest(const UUIDv4::UUID& userId,
                                           const UUIDv4::UUID& requesterId) const {
        auto friendship = friendshipRepo->find(requesterId, userId);
        if(!friendship)
            return AcceptRequestResult::REQUEST_NOT_FOUND;

        if(friendship->status != FriendshipStatus::PENDING)
            return AcceptRequestResult::ALREADY_PROCESSED;

        return friendshipRepo->updateStatus(requesterId, userId, FriendshipStatus::REJECTED)
            ? AcceptRequestResult::SUCCESS
            : AcceptRequestResult::REQUEST_NOT_FOUND;
    }

    std::vector<UUIDv4::UUID> getFriends(const UUIDv4::UUID& userId) const {
        return friendshipRepo->getFriends(userId);
    }

    std::vector<Friendship> getPendingRequests(const UUIDv4::UUID& userId) const {
        return friendshipRepo->getPendingRequests(userId);
    }
};
