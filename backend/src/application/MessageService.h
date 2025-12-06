#pragma once
#include <memory>
#include <random>
#include "../domain/message/MessageRepository.h"
#include "../domain/group/GroupRepository.h"
#include "../domain/user/UserRepository.h"
#include "../domain/friendship/FriendshipRepository.h"
#include "../exceptions/user_not_found_error.h"
#include "../exceptions/group_not_found_error.h"
#include "../exceptions/not_group_member_error.h"
#include "NotificationService.h"

class MessageService {
    std::shared_ptr<MessageRepository> messageRepo;
    std::shared_ptr<GroupRepository> groupRepo;
    std::shared_ptr<UserRepository> userRepo;
    std::shared_ptr<FriendshipRepository> friendshipRepo;
    std::shared_ptr<NotificationService> notificationService;
    UUIDv4::UUIDGenerator<std::mt19937_64> uuidGenerator;

public:
    MessageService(std::shared_ptr<MessageRepository> mRepo,
                   std::shared_ptr<GroupRepository> gRepo,
                   std::shared_ptr<UserRepository> uRepo,
                   std::shared_ptr<FriendshipRepository> fRepo,
                   std::shared_ptr<NotificationService> nService)
        : messageRepo(std::move(mRepo)),
          groupRepo(std::move(gRepo)),
          userRepo(std::move(uRepo)),
          friendshipRepo(std::move(fRepo)),
          notificationService(std::move(nService)) {}

    // Wysyłanie wiadomości do grupy
    UUIDv4::UUID sendGroupMessage(const UUIDv4::UUID& senderId,
                                  const UUIDv4::UUID& groupId,
                                  const std::string& content) {
        // Sprawdź czy nadawca istnieje
        if(!userRepo->exists(senderId))
            throw user_not_found_error();

        // Sprawdź czy grupa istnieje
        const auto group = groupRepo->findById(groupId);
        if(!group.has_value())
            throw group_not_found_error();

        // Sprawdź czy nadawca jest członkiem grupy
        if(!groupRepo->isMember(groupId, senderId))
            throw not_group_member_error();

        const auto now = std::chrono::system_clock::now();
        const auto messageId = uuidGenerator.getUUID();

        const Message message{
            messageId,
            senderId,
            groupId,
            MessageType::GROUP,
            content,
            now,
            now
        };

        if(!messageRepo->save(message))
            throw std::runtime_error("Failed to send message");

        // Wyślij notyfikację do wszystkich członków grupy (oprócz nadawcy)
        notifyGroupMembers(group.value(), senderId, message);

        return messageId;
    }

    // Wysyłanie wiadomości prywatnej do przyjaciela
    UUIDv4::UUID sendPrivateMessage(const UUIDv4::UUID& senderId,
                                    const UUIDv4::UUID& receiverId,
                                    const std::string& content) {
        // Sprawdź czy nadawca istnieje
        if(!userRepo->exists(senderId))
            throw user_not_found_error();

        // Sprawdź czy odbiorca istnieje
        if(!userRepo->exists(receiverId))
            throw user_not_found_error();

        // Sprawdź czy są znajomymi
        if(!friendshipRepo->areFriends(senderId, receiverId))
            throw std::runtime_error("Users are not friends");

        const auto now = std::chrono::system_clock::now();
        const auto messageId = uuidGenerator.getUUID();

        const Message message{
            messageId,
            senderId,
            receiverId,
            MessageType::PRIVATE,
            content,
            now,
            now
        };

        if(!messageRepo->save(message))
            throw std::runtime_error("Failed to send message");

        // Wyślij notyfikację do odbiorcy
        notifyPrivateMessage(receiverId, message);

        return messageId;
    }

    // Pobieranie wiadomości grupowych
    std::vector<Message> getGroupMessages(const UUIDv4::UUID& groupId,
                                         const UUIDv4::UUID& userId,
                                         const std::chrono::system_clock::time_point& since,
                                         size_t limit = 100,
                                         size_t offset = 0) const {
        // Sprawdź czy użytkownik istnieje
        if(!userRepo->exists(userId))
            throw user_not_found_error();

        // Sprawdź czy grupa istnieje
        const auto group = groupRepo->findById(groupId);
        if(!group.has_value())
            throw group_not_found_error();

        // Sprawdź czy użytkownik jest członkiem grupy
        if(!groupRepo->isMember(groupId, userId))
            throw not_group_member_error();

        return messageRepo->findMessagesByReceiverId(groupId, since, limit, offset);
    }

    // Pobieranie ostatnich wiadomości grupowych (domyślnie 100)
    std::vector<Message> getRecentGroupMessages(const UUIDv4::UUID& groupId,
                                               const UUIDv4::UUID& userId,
                                               size_t limit = 100) const {
        // Pobierz wiadomości z ostatnich 30 dni
        const auto since = std::chrono::system_clock::now() - std::chrono::hours(24 * 30);
        return getGroupMessages(groupId, userId, since, limit, 0);
    }

    // Pobieranie wiadomości prywatnych między dwoma użytkownikami
    std::vector<Message> getPrivateMessages(const UUIDv4::UUID& user1Id,
                                           const UUIDv4::UUID& user2Id,
                                           const std::chrono::system_clock::time_point& since,
                                           size_t limit = 100,
                                           size_t offset = 0) const {
        // Sprawdź czy obaj użytkownicy istnieją
        if(!userRepo->exists(user1Id))
            throw user_not_found_error();
        if(!userRepo->exists(user2Id))
            throw user_not_found_error();

        // Sprawdź czy są znajomymi
        if(!friendshipRepo->areFriends(user1Id, user2Id))
            throw std::runtime_error("Users are not friends");

        return messageRepo->findPrivateMessages(user1Id, user2Id, since, limit, offset);
    }

    // Pobieranie ostatnich wiadomości prywatnych (domyślnie 100)
    std::vector<Message> getRecentPrivateMessages(const UUIDv4::UUID& user1Id,
                                                 const UUIDv4::UUID& user2Id,
                                                 size_t limit = 100) const {
        // Pobierz wiadomości z ostatnich 30 dni
        const auto since = std::chrono::system_clock::now() - std::chrono::hours(24 * 30);
        return getPrivateMessages(user1Id, user2Id, since, limit, 0);
    }

private:
    // Notyfikacja członków grupy o nowej wiadomości
    void notifyGroupMembers(const Group& group, const UUIDv4::UUID& senderId, const Message& message) const {
        nlohmann::json notification;
        notification["type"] = "NEW_GROUP_MESSAGE";
        notification["messageId"] = message.messageId.str();
        notification["senderId"] = message.senderId.str();
        notification["groupId"] = message.receiverId.str();
        notification["content"] = message.content;
        notification["sentAt"] = std::chrono::system_clock::to_time_t(message.sentAt);

        // Wyślij do wszystkich członków oprócz nadawcy
        for(const auto& memberId : group.members) {
            if(memberId != senderId) {
                notificationService->sendNotification(memberId, notification);
            }
        }
    }

    // Notyfikacja o nowej wiadomości prywatnej
    void notifyPrivateMessage(const UUIDv4::UUID& receiverId, const Message& message) const {
        nlohmann::json notification;
        notification["type"] = "NEW_PRIVATE_MESSAGE";
        notification["messageId"] = message.messageId.str();
        notification["senderId"] = message.senderId.str();
        notification["content"] = message.content;
        notification["sentAt"] = std::chrono::system_clock::to_time_t(message.sentAt);

        notificationService->sendNotification(receiverId, notification);
    }
};
