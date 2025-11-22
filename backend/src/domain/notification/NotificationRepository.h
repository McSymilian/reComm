#pragma once

#include <vector>
#include <nlohmann/json.hpp>
#include "uuid_v4.h"

using json = nlohmann::json;

struct PendingNotification {
    UUIDv4::UUID userId;
    json notification;
    std::chrono::system_clock::time_point createdAt;
};

class NotificationRepository {
public:
    virtual ~NotificationRepository() = default;

    virtual bool save(const PendingNotification& notification) = 0;
    virtual std::vector<PendingNotification> getPendingForUser(const UUIDv4::UUID& userId) = 0;
    virtual bool clearForUser(const UUIDv4::UUID& userId) = 0;
};

