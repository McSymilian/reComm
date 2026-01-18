#pragma once

#include <chrono>
#include <string>
#include "uuid_v4.h"

enum class MessageType {
    PRIVATE,
    GROUP
};

struct Message {
    UUIDv4::UUID messageId;
    UUIDv4::UUID senderId;
    UUIDv4::UUID receiverId;
    MessageType type;
    std::string senderName;
    std::string content;
    std::chrono::system_clock::time_point sentAt;
    std::chrono::system_clock::time_point deliveredAt;

     std::string getConversationId() const {
         if (type == MessageType::GROUP)
            return receiverId.str();

         const std::string sender = senderId.str();
         const std::string receiver = receiverId.str();
         return sender < receiver ? sender + "_" + receiver : receiver + "_" + sender;
    }
};