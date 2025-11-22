#pragma once

#include <unordered_map>
#include <mutex>
#include <memory>
#include <nlohmann/json.hpp>
#include "uuid_v4.h"
#include "../utils/Logger.h"

using json = nlohmann::json;

struct ClientConnection {
    int socket;
    UUIDv4::UUID userId;
    std::mutex sendMutex;
};

class ConnectionManager {
    std::unordered_map<std::string, std::shared_ptr<ClientConnection>> connections;
    mutable std::mutex connectionsMutex;

public:
    void registerConnection(const UUIDv4::UUID& userId, int socket) {
        std::lock_guard<std::mutex> lock(connectionsMutex);

        auto connection = std::make_shared<ClientConnection>();
        connection->socket = socket;
        connection->userId = userId;

        connections[userId.str()] = connection;
        Logger::log(std::format("Registered connection for user {}", userId.str()), Logger::Level::INFO, Logger::Importance::LOW);
    }

    void unregisterConnection(const UUIDv4::UUID& userId) {
        std::lock_guard<std::mutex> lock(connectionsMutex);
        connections.erase(userId.str());
        Logger::log(std::format("Unregistered connection for user {}", userId.str()), Logger::Level::INFO, Logger::Importance::LOW);
    }

    bool sendNotification(const UUIDv4::UUID& userId, const json& notification) {
        std::shared_ptr<ClientConnection> connection;

        {
            std::lock_guard<std::mutex> lock(connectionsMutex);
            auto it = connections.find(userId.str());
            if(it == connections.end()) {
                return false;
            }
            connection = it->second;
        }

        std::lock_guard<std::mutex> sendLock(connection->sendMutex);

        std::string notificationStr = notification.dump() + "\n";
        ssize_t sent = send(connection->socket, notificationStr.c_str(), notificationStr.size(), 0);

        if(sent == -1) {
            Logger::log(std::format("Failed to send notification to user {}", userId.str()), Logger::Level::WARNING, Logger::Importance::MEDIUM);
            return false;
        }

        Logger::log(std::format("Sent notification to user {}: {}", userId.str(), notificationStr), Logger::Level::INFO, Logger::Importance::LOW);
        return true;
    }

    bool isUserConnected(const UUIDv4::UUID& userId) const {
        std::lock_guard<std::mutex> lock(connectionsMutex);
        return connections.find(userId.str()) != connections.end();
    }
};

