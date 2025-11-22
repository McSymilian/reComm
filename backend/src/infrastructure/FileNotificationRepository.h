#pragma once

#include <fstream>
#include <filesystem>
#include <mutex>
#include "../domain/notification/NotificationRepository.h"
#include "../utils/Logger.h"

class FileNotificationRepository final : public NotificationRepository {
    const std::string dbPath;
    mutable std::mutex fileMutex;

    std::string getFilePath(const UUIDv4::UUID& userId) const {
        return dbPath + "/notifications_" + userId.str() + ".json";
    }

public:
    explicit FileNotificationRepository(std::string dbPath) : dbPath(std::move(dbPath)) {
        std::filesystem::create_directories(this->dbPath);
    }

    bool save(const PendingNotification& notification) override {
        std::lock_guard<std::mutex> lock(fileMutex);

        const std::string filePath = getFilePath(notification.userId);
        json notifications = json::array();

        if(std::filesystem::exists(filePath)) {
            std::ifstream file(filePath);
            if(file.is_open()) {
                try {
                    file >> notifications;
                } catch(const std::exception& e) {
                    Logger::log(std::format("Error reading notifications file: {}", e.what()), Logger::Level::ERROR, Logger::Importance::MEDIUM);
                    notifications = json::array();
                }
                file.close();
            }
        }

        json notificationJson;
        notificationJson["notification"] = notification.notification;
        notificationJson["createdAt"] = std::chrono::system_clock::to_time_t(notification.createdAt);

        notifications.push_back(notificationJson);

        std::ofstream outFile(filePath);
        if(!outFile.is_open()) {
            Logger::log(std::format("Could not open notifications file for writing: {}", filePath), Logger::Level::ERROR, Logger::Importance::HIGH);
            return false;
        }

        outFile << notifications.dump(4);
        outFile.close();

        return true;
    }

    std::vector<PendingNotification> getPendingForUser(const UUIDv4::UUID& userId) override {
        std::lock_guard<std::mutex> lock(fileMutex);

        std::vector<PendingNotification> result;
        const std::string filePath = getFilePath(userId);

        if(!std::filesystem::exists(filePath)) {
            return result;
        }

        std::ifstream file(filePath);
        if(!file.is_open()) {
            return result;
        }

        try {
            json notifications;
            file >> notifications;
            file.close();

            for(const auto& notifJson : notifications) {
                PendingNotification notif;
                notif.userId = userId;
                notif.notification = notifJson["notification"];

                if(notifJson.contains("createdAt")) {
                    auto timeT = notifJson["createdAt"].get<std::time_t>();
                    notif.createdAt = std::chrono::system_clock::from_time_t(timeT);
                } else {
                    notif.createdAt = std::chrono::system_clock::now();
                }

                result.push_back(notif);
            }
        } catch(const std::exception& e) {
            Logger::log(std::format("Error parsing notifications file: {}", e.what()), Logger::Level::ERROR, Logger::Importance::MEDIUM);
        }

        return result;
    }

    bool clearForUser(const UUIDv4::UUID& userId) override {
        std::lock_guard<std::mutex> lock(fileMutex);

        const std::string filePath = getFilePath(userId);

        if(std::filesystem::exists(filePath)) {
            return std::filesystem::remove(filePath);
        }

        return true;
    }
};

