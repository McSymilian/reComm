#pragma once
#include "../domain/group/GroupRepository.h"
#include "../domain/friendship/FriendshipRepository.h"
#include "../domain/user/UserRepository.h"
#include "../exceptions/group_not_found_error.h"
#include "../exceptions/not_group_member_error.h"
#include "../exceptions/user_not_found_error.h"
// #include "../exceptions/already_group_member_error.h"
#include "../exceptions/cannot_add_non_friend_to_group_error.h"
#include "../exceptions/user_already_in_group_error.h"
#include "../exceptions/cannot_leave_group_as_last_member_error.h"
#include <memory>
#include <random>

class GroupService {
    std::shared_ptr<GroupRepository> groupRepo;
    std::shared_ptr<FriendshipRepository> friendshipRepo;
    std::shared_ptr<UserRepository> userRepo;
    UUIDv4::UUIDGenerator<std::mt19937_64> uuidGenerator;

public:
    GroupService(std::shared_ptr<GroupRepository> gRepo,
                 std::shared_ptr<FriendshipRepository> fRepo,
                 std::shared_ptr<UserRepository> uRepo)
        : groupRepo(std::move(gRepo)),
          friendshipRepo(std::move(fRepo)),
          userRepo(std::move(uRepo)) {}

    UUIDv4::UUID createGroup(const UUIDv4::UUID& creatorId, const std::string& groupName) {
        if(!userRepo->exists(creatorId))
            throw user_not_found_error();

        const auto now = std::chrono::system_clock::now();
        const auto groupId = uuidGenerator.getUUID();

        const Group group{
            groupId,
            groupName,
            creatorId,
            {creatorId},
            now,
            now
        };

        if(!groupRepo->save(group))
            throw std::runtime_error("Failed to create group");

        return groupId;
    }

    void addMemberToGroup(const UUIDv4::UUID& groupId,
                         const UUIDv4::UUID& adderId,
                         const std::string& newMemberUsername) const {
        const auto group = groupRepo->findById(groupId);
        if(!group.has_value())
            throw group_not_found_error();

        if(!groupRepo->isMember(groupId, adderId))
            throw not_group_member_error();

        const auto newMember = userRepo->findByUsername(newMemberUsername);
        if(!newMember.has_value())
            throw user_not_found_error();

        if(groupRepo->isMember(groupId, newMember->uuid))
            throw user_already_in_group_error();

        if(!friendshipRepo->areFriends(adderId, newMember->uuid))
            throw cannot_add_non_friend_to_group_error();

        if(!groupRepo->addMember(groupId, newMember->uuid))
            throw std::runtime_error("Failed to add member to group");
    }

    void updateGroupName(const UUIDv4::UUID& groupId,
                        const UUIDv4::UUID& userId,
                        const std::string& newName) const {
        const auto group = groupRepo->findById(groupId);
        if(!group.has_value())
            throw group_not_found_error();

        if(!groupRepo->isMember(groupId, userId))
            throw not_group_member_error();

        if(!groupRepo->updateName(groupId, newName))
            throw std::runtime_error("Failed to update group name");
    }

    void leaveGroup(const UUIDv4::UUID& groupId, const UUIDv4::UUID& userId) const {
        const auto group = groupRepo->findById(groupId);
        if(!group.has_value())
            throw group_not_found_error();

        if(!groupRepo->isMember(groupId, userId))
            throw not_group_member_error();

        if(group->members.size() == 1)
            throw cannot_leave_group_as_last_member_error();

        if(!groupRepo->removeMember(groupId, userId))
            throw std::runtime_error("Failed to leave group");
    }

    void deleteGroup(const UUIDv4::UUID& groupId, const UUIDv4::UUID& userId) const {
        const auto group = groupRepo->findById(groupId);
        if(!group.has_value())
            throw group_not_found_error();

        if (!groupRepo->isMember(groupId, userId))
            throw not_group_member_error();

        if(!groupRepo->deleteGroup(groupId))
            throw std::runtime_error("Failed to delete group");
    }

    std::vector<Group> getUserGroups(const UUIDv4::UUID& userId) const {
        if(!userRepo->exists(userId))
            throw user_not_found_error();

        return groupRepo->findByMemberId(userId);
    }

    std::optional<Group> getGroupDetails(const UUIDv4::UUID& groupId, const UUIDv4::UUID& userId) const {
        auto group = groupRepo->findById(groupId);
        if(!group.has_value())
            return std::nullopt;

        if(!groupRepo->isMember(groupId, userId))
            throw not_group_member_error();

        return group;
    }

    std::vector<UUIDv4::UUID> getGroupMembers(const UUIDv4::UUID& groupId, const UUIDv4::UUID& userId) const {
        auto group = groupRepo->findById(groupId);
        if(!group.has_value())
            throw group_not_found_error();

        if(!groupRepo->isMember(groupId, userId))
            throw not_group_member_error();

        return group->members;
    }
};

