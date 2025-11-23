#pragma once
#include "../domain/user/User.h"
#include "../domain/user/UserRepository.h"
#include "JwtService.h"
#include <memory>
#include <string>
#include <openssl/sha.h>
#include <iomanip>
#include <sstream>
#include <optional>

class UserService {
    const std::shared_ptr<UserRepository> repository;
    const std::shared_ptr<JwtService> jwtService;
    UUIDv4::UUIDGenerator<std::mt19937_64> uuidGenerator;

    static std::string hashPassword(const std::string& password) {
        unsigned char hash[SHA256_DIGEST_LENGTH];
        SHA256(reinterpret_cast<const unsigned char*>(password.c_str()),
               password.length(), hash);

        std::stringstream ss;
        for(unsigned char i : hash) {
            ss << std::hex << std::setw(2) << std::setfill('0')
               << static_cast<int>(i);
        }
        return ss.str();
    }

public:
    explicit UserService(std::shared_ptr<UserRepository> repo,
                        std::shared_ptr<JwtService> jwt)
        : repository(std::move(repo)), jwtService(std::move(jwt)) {}

    std::optional<std::string> registerUser(const std::string& username, const std::string& password) {
        if(repository->exists(username))
            return std::nullopt;

        const User user {
            username,
            hashPassword(password),
            uuidGenerator.getUUID()
        };
        if (repository->save(user))
            return jwtService->generateToken(user.uuid.str());

        return std::nullopt;
    }

    std::optional<std::string> authenticate(const std::string& username, const std::string& password) const {
        const std::optional<User> user = repository->findByUsername(username);
        if(!user.has_value()) return std::nullopt;

        if(user->passwordHash != hashPassword(password))
            return std::nullopt;

        return jwtService->generateToken(user->uuid.str());
    }

    std::optional<User> getUserByUsername(const std::string& username) const {
        return repository->findByUsername(username);
    }

    std::optional<User> getUserByUuid(const UUIDv4::UUID& uuid) const {
        return repository->findByUUID(uuid);
    }
};
