#pragma once
#include <string>
#include <ctime>
#include <boost/date_time/posix_time/posix_time.hpp>
#include <boost/date_time/local_time/local_time.hpp>

// constexpr auto version = L"nightly 2025-01-05";
constexpr const auto* group_text = L"「TCAA 汉化组，版本: {}」";
constexpr const auto* version_text = L"Alpha {}";

std::string convertUnixTimestamp(std::time_t unix_time);

std::wstring version_string();
