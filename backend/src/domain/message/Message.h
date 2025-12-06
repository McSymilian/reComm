#pragma once

#include <chrono>
#include <string>
#include "uuid_v4.h"

enum class MessageType {
    PRIVATE,  // Wiadomość prywatna (między dwoma użytkownikami)
    GROUP     // Wiadomość grupowa
};

struct Message {
    UUIDv4::UUID messageId;
    UUIDv4::UUID senderId;
    UUIDv4::UUID receiverId;  // Dla wiadomości prywatnych - ID odbiorcy, dla grupowych - ID grupy
    MessageType type;
    std::string content;
    std::chrono::system_clock::time_point sentAt;
    std::chrono::system_clock::time_point deliveredAt;

    // Helper method to get conversation ID (sortowane UUID dla prywatnych konwersacji)
    [[nodiscard]] std::string getConversationId() const {
        if (type == MessageType::GROUP) {
            return receiverId.str();
        }
        // Dla prywatnych - sortujemy UUID aby zawsze mieć ten sam ID konwersacji
        const std::string sender = senderId.str();
        const std::string receiver = receiverId.str();
        return sender < receiver ? sender + "_" + receiver : receiver + "_" + sender;
    }
};