#pragma once

#include <string>
#include <optional>
#include <jwt-cpp/jwt.h>
#include <chrono>
#include <algorithm>
#include <cctype>

class JwtService {
    const std::string jwtSecret;

    static std::string cleanToken(const std::string& token) {
        std::string cleaned = token;
        cleaned.erase(std::ranges::remove_if(cleaned,
        [](const unsigned char c) { return std::isspace(c); }).begin(), cleaned.end()
        );
        return cleaned;
    }

public:
    explicit JwtService(std::string secret)
        : jwtSecret(std::move(secret)) {}

    std::string generateToken(const std::string& uuid) const {
        const auto now = std::chrono::system_clock::now();
        const auto expiration = now + std::chrono::hours(12);

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
            const std::string cleanedToken = cleanToken(token);

            const auto verifier = jwt::verify()
                    .allow_algorithm(jwt::algorithm::hs256{jwtSecret})
                    .with_issuer("reComm");

            const auto decoded = jwt::decode(cleanedToken);
            verifier.verify(decoded);
            return true;
        } catch(const jwt::error::token_verification_exception&) {
            return false;
        } catch(const std::exception&) {
            return false;
        }
    }

    static std::optional<UUIDv4::UUID> getUuidFromToken(const std::string& token) {
        try {
            const std::string cleanedToken = cleanToken(token);
            const auto decoded = jwt::decode(cleanedToken);
            return UUIDv4::UUID::fromStrFactory(decoded.get_payload_claim("uuid").as_string());
        } catch(const std::exception&) {
            return std::nullopt;
        }
    }
};
