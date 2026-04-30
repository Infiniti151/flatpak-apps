# flatpak-apps
Collection of Flatpak apps available as RPM through COPR (for Fedora Linux)

## App List

| App | Source | Version | COPR Build Status |
| :------: | :------: | :------: | :------: |
| text-compare | [josephmawa/TextCompare](https://github.com/josephmawa/TextCompare) | 0.1.11 | [![COPR Build Status](https://img.shields.io/badge/dynamic/json?url=https://copr.fedorainfracloud.org/api_3/build/list/%3Fownername%3Dinfiniti151%26projectname%3Dflatpak-apps%26packagename%3Dtext-compare%26limit%3D1&query=$.items[0].state&label=COPR&style=for-the-badge&logo=fedora&logoColor=white)](https://copr.fedorainfracloud.org/coprs/infiniti151/flatpak-apps/package/text-compare/)  |
| concessio | [ronniedroid/concessio](https://github.com/ronniedroid/concessio) | 0.3.0 | [![COPR Build Status](https://img.shields.io/badge/dynamic/json?url=https://copr.fedorainfracloud.org/api_3/build/list/%3Fownername%3Dinfiniti151%26projectname%3Dflatpak-apps%26packagename%3Dconcessio%26limit%3D1&query=$.items[0].state&label=COPR&style=for-the-badge&logo=fedora&logoColor=white)](https://copr.fedorainfracloud.org/coprs/infiniti151/flatpak-apps/package/concessio/) |

## Installation
1. Enable COPR repo
   
   `sudo dnf copr enable infiniti151/flatpak-apps`
3. Install app
   
   `sudo dnf install <app>`
