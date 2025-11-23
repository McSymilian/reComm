#pragma once

#include <memory>
#include <nlohmann/json.hpp>
#include "../domain/notification/NotificationRepository.h"
#include "../infrastructure/ConnectionManager.h"

using json = nlohmann::json;

class NotificationService {
    std::shared_ptr<NotificationRepository> notificationRepository;
    std::shared_ptr<ConnectionManager> connectionManager;

public:
    NotificationService(
        std::shared_ptr<NotificationRepository> notificationRepository,
        std::shared_ptr<ConnectionManager> connectionManager
    ) : notificationRepository(std::move(notificationRepository)),
        connectionManager(std::move(connectionManager)) {}

    void sendNotification(const UUIDv4::UUID& userId, const json& notification) const {
        if(connectionManager->isUserConnected(userId)) {
            if(connectionManager->sendNotification(userId, notification)) {
                Logger::log(std::format("Sent live notification to user {}", userId.str()), Logger::Level::INFO, Logger::Importance::LOW);
                return;
            }
        }

        PendingNotification pending;
        pending.userId = userId;
        pending.notification = notification;
        pending.createdAt = std::chrono::system_clock::now();

        if(notificationRepository->save(pending)) {
            Logger::log(std::format("Saved pending notification for user {}", userId.str()), Logger::Level::INFO, Logger::Importance::LOW);
        } else {
            Logger::log(std::format("Failed to save notification for user {}", userId.str()), Logger::Level::ERROR, Logger::Importance::HIGH);
        }
    }

    std::vector<PendingNotification> getPendingNotifications(const UUIDv4::UUID& userId) const {
        return notificationRepository->getPendingForUser(userId);
    }

    void clearPendingNotifications(const UUIDv4::UUID& userId) const {
        notificationRepository->clearForUser(userId);
    }

    void sendPendingNotifications(const UUIDv4::UUID& userId) const {
        const auto pendingNotifications = getPendingNotifications(userId);

        if(pendingNotifications.empty()) {
            return;
        }

        Logger::log(std::format("Sending {} pending notifications to user {}", pendingNotifications.size(), userId.str()), Logger::Level::INFO, Logger::Importance::MEDIUM);

        for(const auto& pending : pendingNotifications) {
            connectionManager->sendNotification(userId, pending.notification);
        }

        clearPendingNotifications(userId);
    }
};

