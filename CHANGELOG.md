# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to [Semantic Versioning](http://semver.org/).

## [2.0.0] - 2019-05-21
#### Added
- Support for python 3.7 | [6f02f8d](https://github.com/actmd/elementium/commit/6f02f8dc0a305176bbfe3c1dfc1a2fd5abc22146)
- Removed support for python 3.3
- Bumped major version number to indicate potential for breaking due to parameter renaming.

### Changed
- README
- Renamed `async` parameters to `asynchronous` for python 3.7 compatibility.

## [1.11.0] - 2017-10-02
#### Added
- Support for python 3.6 | [a541344](https://github.com/actmd/elementium/commit/a541344da164f2f647fe78701b19bc4c949a9a98)

### Changed
- README
- Modified how metaclasses were registered
- Removed support for python 3.2


## [1.1.10] - 2 Oct 2017
### Changed
- Versions updated | [253c9ef](https://github.com/actmd/elementium/commit/253c9efadda370a7132eeff94e6b26ba6ff76e75)

### Bugfixes
- Documentation fix | [438d580](https://github.com/actmd/elementium/commit/438d580dd9395b75c8d5a37251b4857718faa2dc)


## [1.1.9] - 2 Oct 2017
### Changed
- Versions updated | [253c9ef](https://github.com/actmd/elementium/commit/253c9efadda370a7132eeff94e6b26ba6ff76e75)


## [1.1.8] - 2 Oct 2017
### Added
- More six tests | [b5f035a](https://github.com/actmd/elementium/commit/b5f035a95d42e9456909524ea342f056f1229b5b)


## [1.1.7] - 18 Aug 2016
#### Added
- Tests added | [8156fa4](https://github.com/actmd/elementium/commit/8156fa4bdbd8104792a3d6c5258ad0640f70f36e)


## [1.1.6] - 3 Dec 2015
### Changed
- Added a couple of usage examples in Lazy load Element items | [dff9561](https://github.com/actmd/elementium/commit/dff95615ab772e62eb3338a026c607defa43d865)


## [1.1.5] - 19 Nov 2015
### Bugfixes
- Add build status to README | [74c1b91](https://github.com/actmd/elementium/commit/74c1b91f5a12b238a6b429608fac69d5e5183460)


## [1.1.4] - 19 Nov 2015
### Bugfixes
- Add Travis CI config file and fixes for Python 3 compatability | [d3e9fc1](https://github.com/actmd/elementium/commit/d3e9fc1ac2422e39e45b0d3ee8bbd3bde3017629)


## [1.1.3] - 6 Nov 2015
### Bugfixes
- verion information incorrect | [ab273be](https://github.com/actmd/elementium/commit/ab273bed25ba83e966c2068a4cc6f70f2035bad6)


## [1.1.2] - 6 Nov 2015
### Bugfixes
- select() does not accept i=0 | [8d0da69](https://github.com/actmd/elementium/commit/8d0da69b279c9626118767b20c1c86b76183e76f)


## [1.1.1] - 15 May 2015
### Bugfixes
- Error ExceptionRetryElementsWaiter wait() not executed | [458b20a](https://github.com/actmd/elementium/commit/458b20a3782438014e1d853d991b3fe6e652fcbc)


## [1.1.0] - 4 Jan 2015
#### Added
- Created new Waiter subclasses | [30826bf](https://github.com/actmd/elementium/commit/30826bf8b39bd0f754b8d6e28507701ba0e12cdb)

### Changed
- Removed the helper with_update(), with_retry() functions from elements.elements.py and replaced them with the new Waiters
- Removed with_update() and with_retry() methods from the Elements classes and replaced it with a more generic, retried() method
- Reorganized and cleaned up some code


## [1.0.3] - 11 Jul 2014
### Bugfixes
- Map returns | [#](https://github.com/actmd/elementium/commit/8cbfaf955aee7c8b7abc2e0e02d7ba6d7d70bff7)


## [1.0.2] - 10 Jul 2014
### Bugfixes
- Filter returns | [dbcf774](https://github.com/actmd/elementium/commit/dbcf774e6a6605f6483f75a289b4965ca3aa9362)


## [1.0.1] - 10 Jul 2014
### Bugfixes
- Wrong `self` assignment | [62721ae](https://github.com/actmd/elementium/commit/62721ae806802e45fd2fb8d8190c908a4b37072d)


## [1.0.0] - 01 Jul 2014
#### Added
- Initial commit | [8472dbc](https://github.com/actmd/elementium/commit/8472dbc0614b0baa93a843802f0837cc232b1989)
