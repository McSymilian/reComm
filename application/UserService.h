#pragma once
#include "../domain/User.h"
#include "../domain/UserRepository.h"
#include <memory>
#include <string>
#include <openssl/sha.h>
#include <iomanip>
#include <sstream>
#include <jwt-cpp/jwt.h>
#include <chrono>

class UserService {
    std::shared_ptr<UserRepository> repository;
    UUIDv4::UUIDGenerator<std::mt19937_64> uuidGenerator;
    std::string jwtSecret;

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

    std::string generateToken(const std::string& uuid) const {
        auto now = std::chrono::system_clock::now();
        auto expiration = now + std::chrono::hours(12);

        auto token = jwt::create()
                .set_issuer("reComm")
                .set_type("JWT")
                .set_payload_claim("uuid", jwt::claim(uuid))
                .set_issued_at(now)
                .set_expires_at(expiration)
                .sign(jwt::algorithm::hs256{jwtSecret});

        return token;
    }
    
public:
    explicit UserService(std::shared_ptr<UserRepository> repo, std::string secret = "your-secret-key-change-in-production")
        : repository(std::move(repo)), jwtSecret(std::move(secret)) {}
    
    std::optional<std::string> registerUser(const std::string& username, const std::string& password) {
        if(repository->exists(username))
            return std::nullopt;


        const User user {
            username,
            hashPassword(password),
            uuidGenerator.getUUID()
        };
        if (repository->save(user))
            return generateToken(username);

        return std::nullopt;
    }
    
    std::optional<std::string> authenticate(const std::string& username, const std::string& password) {
        auto user = repository->findByUsername(username);
        if(!user) return std::nullopt;
        
        if(user->passwordHash != hashPassword(password))
            return std::nullopt;

        return generateToken(user->uuid.str());
    }

    bool verifyToken(const std::string& token) const {
        try {
            const auto verifier = jwt::verify()
                    .allow_algorithm(jwt::algorithm::hs256{jwtSecret})
                    .with_issuer("reComm");

            const auto decoded = jwt::decode(token);
            verifier.verify(decoded);
            return true;
        } catch(const std::exception&) {
            return false;
        }
    }

    static std::optional<std::string> getUuidFromToken(const std::string& token) {
        try {
            const auto decoded = jwt::decode(token);
            return decoded.get_payload_claim("uuid").as_string();
        } catch(const std::exception&) {
            return std::nullopt;
        }
    }
    
    std::vector<std::string> getFriends(const std::string& username) {
        // TODO: Implementacja logiki znajomych
        return {};
    }
};
