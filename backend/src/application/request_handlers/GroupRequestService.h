#pragma once
#include <nlohmann/json.hpp>
#include <memory>

#include "RequestService.h"
#include "../GroupService.h"
#include "../../domain/user/UserRepository.h"
#include "../../exceptions/invalid_token_error.h"
#include "../../exceptions/missing_required_field_error.h"

using json = nlohmann::json;

class CreateGroupService final : public RequestService {
    const std::shared_ptr<GroupService> groupService;

public:
    explicit CreateGroupService(
        std::shared_ptr<GroupService> groupService
    ) : groupService(std::move(groupService)) {}

    std::string getHandledMethodName() override {
        return "CREATE_GROUP";
    }

    json handleRequest(const json& request, const UUIDv4::UUID userUUID) override {
        const std::string groupName = request.value("groupName", "");

        if (groupName.empty())
            throw missing_required_field_error("groupName");

        const auto groupId = groupService->createGroup(userUUID, groupName);

        json response;
        response["code"] = 200;
        response["message"] = "Group created successfully";
        response["groupId"] = groupId.str();
        return response;
    }
};

class AddMemberToGroupService final : public RequestService {
    const std::shared_ptr<GroupService> groupService;

public:
    explicit AddMemberToGroupService(
        std::shared_ptr<GroupService> groupService
    ) : groupService(std::move(groupService)) {}

    std::string getHandledMethodName() override {
        return "ADD_MEMBER_TO_GROUP";
    }

    json handleRequest(const json& request, const UUIDv4::UUID userUUID) override {
        const std::string groupIdStr = request.value("groupId", "");
        const std::string username = request.value("username", "");

        if (groupIdStr.empty())
            throw missing_required_field_error("groupId");
        if (username.empty())
            throw missing_required_field_error("username");

        const auto groupUuid = UUIDv4::UUID::fromStrFactory(groupIdStr);
        if (groupIdStr.size() != 36)
            throw std::runtime_error("Invalid group ID");

        groupService->addMemberToGroup(groupUuid, userUUID, username);

        json response;
        response["code"] = 200;
        response["message"] = "Member added to group successfully";
        return response;
    }
};

class UpdateGroupNameService final : public RequestService {
    const std::shared_ptr<GroupService> groupService;

public:
    explicit UpdateGroupNameService(
        std::shared_ptr<GroupService> groupService
    ) : groupService(std::move(groupService)) {}

    std::string getHandledMethodName() override {
        return "UPDATE_GROUP_NAME";
    }

    json handleRequest(const json& request, const UUIDv4::UUID userUUID) override {
        const std::string groupIdStr = request.value("groupId", "");
        const std::string newName = request.value("newName", "");

        if (groupIdStr.empty())
            throw missing_required_field_error("groupId");
        if (newName.empty())
            throw missing_required_field_error("newName");

        const auto groupUuid = UUIDv4::UUID::fromStrFactory(groupIdStr);
        if (groupIdStr.size() != 36)
            throw std::runtime_error("Invalid group ID");

        groupService->updateGroupName(groupUuid, userUUID, newName);

        json response;
        response["code"] = 200;
        response["message"] = "Group name updated successfully";
        return response;
    }
};

class LeaveGroupService final : public RequestService {
    const std::shared_ptr<GroupService> groupService;

public:
    explicit LeaveGroupService(
        std::shared_ptr<GroupService> groupService
    ) : groupService(std::move(groupService)) {}

    std::string getHandledMethodName() override {
        return "LEAVE_GROUP";
    }

    json handleRequest(const json& request, const UUIDv4::UUID userUUID) override {
        const std::string groupIdStr = request.value("groupId", "");

        if (groupIdStr.empty())
            throw missing_required_field_error("groupId");

        const auto groupUuid = UUIDv4::UUID::fromStrFactory(groupIdStr);
        if (groupIdStr.size() != 36)
            throw std::runtime_error("Invalid group ID");

        groupService->leaveGroup(groupUuid, userUUID);

        json response;
        response["code"] = 200;
        response["message"] = "Left group successfully";
        return response;
    }
};

class DeleteGroupService final : public RequestService {
    const std::shared_ptr<GroupService> groupService;

public:
    explicit DeleteGroupService(
        std::shared_ptr<GroupService> groupService
    ) : groupService(std::move(groupService)) {}

    std::string getHandledMethodName() override {
        return "DELETE_GROUP";
    }

    json handleRequest(const json& request, const UUIDv4::UUID userUUID) override {
        const std::string groupIdStr = request.value("groupId", "");

        if (groupIdStr.empty())
            throw missing_required_field_error("groupId");

        const auto groupUuid = UUIDv4::UUID::fromStrFactory(groupIdStr);
        if (groupIdStr.size() != 36)
            throw std::runtime_error("Invalid group ID");

        groupService->deleteGroup(groupUuid, userUUID);

        json response;
        response["code"] = 200;
        response["message"] = "Group deleted successfully";
        return response;
    }
};

class GetUserGroupsService final : public RequestService {
    const std::shared_ptr<GroupService> groupService;

public:
    explicit GetUserGroupsService(
        std::shared_ptr<GroupService> groupService
    ) : groupService(std::move(groupService)) {}

    std::string getHandledMethodName() override {
        return "GET_USER_GROUPS";
    }

    json handleRequest(const json& request, const UUIDv4::UUID userUUID) override {

        auto groups = groupService->getUserGroups(userUUID);

        json groupsJson = json::array();
        for(const auto& group : groups) {
            groupsJson.push_back(group.toJson());
        }

        json response;
        response["code"] = 200;
        response["groups"] = groupsJson;
        return response;
    }
};

class GetGroupDetailsService final : public RequestService {
    const std::shared_ptr<GroupService> groupService;

public:
    explicit GetGroupDetailsService(
        std::shared_ptr<GroupService> groupService
    ) : groupService(std::move(groupService)) {}

    std::string getHandledMethodName() override {
        return "GET_GROUP_DETAILS";
    }

    json handleRequest(const json& request, const UUIDv4::UUID userUUID) override {
        const std::string groupIdStr = request.value("groupId", "");

        if (groupIdStr.empty())
            throw missing_required_field_error("groupId");

        const auto groupUuid = UUIDv4::UUID::fromStrFactory(groupIdStr);
        if (groupIdStr.size() != 36)
            throw std::runtime_error("Invalid group ID");

        const auto group = groupService->getGroupDetails(groupUuid, userUUID);

        if (!group.has_value()) {
            json response;
            response["code"] = 404;
            response["message"] = "Group not found";
            return response;
        }

        json response;
        response["code"] = 200;
        //todo map memebrs uuids to usernames
        response["group"] = group->toJson();
        return response;
    }
};

class GetGroupMembersService final : public RequestService {
    const std::shared_ptr<GroupService> groupService;
    const std::shared_ptr<UserRepository> userRepo;

public:
    explicit GetGroupMembersService(
        std::shared_ptr<GroupService> groupService,
        std::shared_ptr<UserRepository> userRepo
    ) : groupService(std::move(groupService)),
        userRepo(std::move(userRepo)) {}

    std::string getHandledMethodName() override {
        return "GET_GROUP_MEMBERS";
    }

    json handleRequest(const json& request, const UUIDv4::UUID userUUID) override {
        const std::string groupIdStr = request.value("groupId", "");

        if (groupIdStr.empty())
            throw missing_required_field_error("groupId");

        const auto groupUuid = UUIDv4::UUID::fromStrFactory(groupIdStr);
        if (groupIdStr.size() != 36)
            throw std::runtime_error("Invalid group ID");

        const auto members = groupService->getGroupMembers(groupUuid, userUUID);

        json membersJson = json::array();
        for(const auto& memberId : members) {
            if(auto user = userRepo->findByUUID(memberId)) {
                membersJson.push_back({
                    {"uuid", memberId.str()},
                    {"username", user->username}
                });
            }
        }

        json response;
        response["code"] = 200;
        response["members"] = membersJson;
        return response;
    }
};
