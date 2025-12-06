#pragma once
#include <string>
#include <chrono>

#include "Message.h"
#include "uuid_v4.h"

class MessageRepository {
public:
    virtual ~MessageRepository() = default;
    virtual bool save(const Message& message) = 0;

    // Pobieranie wiadomości grupowych
    virtual std::vector<Message> findMessagesByReceiverId(
        const UUIDv4::UUID& receiverId,
        const std::chrono::system_clock::time_point& since,
        size_t limit,
        size_t offset
    ) = 0;

    // Pobieranie wiadomości prywatnych (między dwoma użytkownikami)
    virtual std::vector<Message> findPrivateMessages(
        const UUIDv4::UUID& user1Id,
        const UUIDv4::UUID& user2Id,
        const std::chrono::system_clock::time_point& since,
        size_t limit,
        size_t offset
    ) = 0;
};