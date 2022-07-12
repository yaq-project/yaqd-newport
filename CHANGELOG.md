# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Added
- newport-conex-agp and newport-smc100 use new trait `has-transformed-position`

## [2021.10.0]

### Changed
- regenerated avpr based on recent traits update

### Fixed
- added forgotten config options to is-daemon: enable, log_level, and log_to_file

## [2021.2.0]

## Added
- conda-forge as installation source

### Fixed
- discard invalid arguments recieved for the same reason invalid messages were written previously
- timing issue which caused daemons to report as "not busy" briefly after a `set_position`

## [2020.11.1]

### Fixed
- discard invalid messages recieved because the device overwrites its own output stream
- premature busy reporting as false while still setting the position

## [2020.11.0]

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

[Unreleased]: https://gitlab.com/yaq/yaqd-newport/-/compare/v2021.10.0...main
[2021.10.0]: https://gitlab.com/yaq/yaqd-newport/-/compare/v2021.2.0...v2021.10.0
[2021.2.0]: https://gitlab.com/yaq/yaqd-newport/-/compare/v2020.11.1...v2021.2.0
[2020.11.1]: https://gitlab.com/yaq/yaqd-newport/-/compare/v2020.11.0...v2020.11.1
[2020.11.0]: https://gitlab.com/yaq/yaqd-newport/-/compare/v2020.07.0...v2020.11.0
[2020.07.0]: https://gitlab.com/yaq/yaqd-newport/-/compare/v2020.05.0...v2020.07.0
[2020.05.0]: https://gitlab.com/yaq/yaqd-newport/-/compare/v0.1.1...v2020.05.0
[0.1.1]: https://gitlab.com/yaq/yaqd-newport/-/compare/v0.1.0...v0.1.1
[0.1.0]: https://gitlab.com/yaq/yaqd-newport/-/tags/v0.1.0
