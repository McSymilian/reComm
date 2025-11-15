#pragma once

#include <string>
#include <optional>
#include <jwt-cpp/jwt.h>
#include <chrono>

class JwtService {
    const std::string jwtSecret;

public:
    explicit JwtService(std::string secret)
        : jwtSecret(std::move(secret)) {}

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

    static std::optional<UUIDv4::UUID> getUuidFromToken(const std::string& token) {
        try {
            const auto decoded = jwt::decode(token);
            return UUIDv4::UUID::fromStrFactory(decoded.get_payload_claim("uuid").as_string());
        } catch(const std::exception&) {
            return std::nullopt;
        }
    }
};
