#pragma once
#include "Group.h"
#include <vector>
#include <optional>

class GroupRepository {
public:
    virtual ~GroupRepository() = default;

    virtual bool save(const Group& group) = 0;
    virtual std::optional<Group> findById(const UUIDv4::UUID& groupId) = 0;
    virtual std::vector<Group> findByMemberId(const UUIDv4::UUID& userId) = 0;
    virtual bool updateName(const UUIDv4::UUID& groupId, const std::string& newName) = 0;
    virtual bool addMember(const UUIDv4::UUID& groupId, const UUIDv4::UUID& memberId) = 0;
    virtual bool removeMember(const UUIDv4::UUID& groupId, const UUIDv4::UUID& memberId) = 0;
    virtual bool isMember(const UUIDv4::UUID& groupId, const UUIDv4::UUID& userId) = 0;
    virtual bool deleteGroup(const UUIDv4::UUID& groupId) = 0;
};

