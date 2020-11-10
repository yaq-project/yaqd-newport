# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Changed
- regenerated avpr based on recent traits update
- new parent class structure

## [2020.07.0]

### Changed
- Implement [YEP-107](https://yeps.yaq.fyi/107) Avro
- Use flit for packaging

### Fixed
- Correct name `baudrate` to `baud_rate`, as specified by the `uses-uart` trait
- No longer uses python 3.8+ only feature named aio tasks
- Apply units from the config

## [2020.05.0]

### Added
- added get_version as described in YEP-105
- added branch information to daemon, package version
- added entry test to gitlab-ci

### Changed
- from now on, yaqd-newport will use calendar-based versioning
- refactored gitlab-ci
- Use daemon level loggers, see [YEP-106](https://yeps.yaq.fyi/106)

## [0.1.1]

### Added
- update readme
- ensure type-hints correct

## [0.1.0]

### Added
- initial release

[Unreleased]: https://gitlab.com/yaq/yaqd-newport/-/compare/v2020.07.0...master
[2020.07.0]: https://gitlab.com/yaq/yaqd-newport/-/compare/v2020.05.0...2020.07.0
[2020.05.0]: https://gitlab.com/yaq/yaqd-newport/-/compare/v0.1.1...v2020.05.0
[0.1.1]: https://gitlab.com/yaq/yaqd-newport/-/compare/v0.1.0...v0.1.1
[0.1.0]: https://gitlab.com/yaq/yaqd-newport/-/tags/v0.1.0
