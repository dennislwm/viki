# viki

<h1 align="center" style="border-bottom: none;">viki</h1>
<h3 align="center">A CLI application that manages servers using a declarative configuration file and a state file.</h3>
<br />
<p align="center">
  <p align="center">
    <a href="https://github.com/dennislwm/viki/issues/new?template=bug_report.yml">Bug report</a>
    ·
    <a href="https://github.com/dennislwm/viki/issues/new?template=feature_request.yml">Feature request</a>
    ·
    <a href="https://github.com/dennislwm/viki/wiki">Read Docs</a>
  </p>
</p>
<br />

---

![GitHub repo size](https://img.shields.io/github/repo-size/dennislwm/viki?style=plastic)
![GitHub language count](https://img.shields.io/github/languages/count/dennislwm/viki?style=plastic)
![GitHub top language](https://img.shields.io/github/languages/top/dennislwm/viki?style=plastic)
![GitHub last commit](https://img.shields.io/github/last-commit/dennislwm/viki?color=red&style=plastic)
![Visitors count](https://hits.sh/github.com/dennislwm/viki/hits.svg)
![GitHub stars](https://img.shields.io/github/stars/dennislwm/viki?style=social)
![GitHub forks](https://img.shields.io/github/forks/dennislwm/viki?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/dennislwm/viki?style=social)
![GitHub followers](https://img.shields.io/github/followers/dennislwm?style=social)

## Purpose

This document describes the `viki` CLI application that manages servers using a declarative configuration file and a state file.

## Audience

The audience for this document includes:

* Developer who will develop the application, run unit tests, configure build tools and write user documentation.

* DevSecOps Engineer who will shape the workflow, and write playbooks and runbooks.

## Why `viki`?

1. Currently, configuration management tools are limited to bash scripts or Ansible, which may not guarantee idempotency. Ansible requires a YAML configuration file that is preprocessed with Jinja syntax, which adds a layer of complexity.

2. The `viki` CLI application is a configuration management tool that ensures idempotency and uses a JSON state file and YAML configuration files.

3. The `viki` CLI application allows the DevSecOps to create a YAML configuration file that specifies the desired outcome for a server, and stores the current state in a JSON state file.

4. The `viki` CLI application allows the Developer to manage command modules, without editing the Python code, by using dictionary constants `DATA_COMMAND` and `MODS_COMMAND`.
  * `DATA_COMMAND` is defined as a JSON object with `<MOD>` and `<CMD>` pairs.
  * `MODS_COMMAND` is defined as a JSON object with `<MOD>` and `{ "insert": "<CMD>", "remove", "<CMD>" }` pairs.

5. The `viki` CLI application supports `sudo` command with both password and passwordless authentication. When `sudo_password` is set to a non-empty string value, password authentication is used instead of passwordless.

## Limitations

This project has several limitations.

* No dependencies between modules and instances of modules.
* You cannot perform an `update` to your resource.
  * You should `destroy` your current resource and `add` a new one.
* No priority when resources are created or destroyed during the `apply` stage.
  * A workaround is to create your configuration files in order, e.g. `01.vk.yaml`, `02.vk.yaml`, and to remove them in the reverse order.
* No support for local server.
  * TODO: When `hostname` is set to `localhost`, the commands will be applied to the current workstation.

## Getting Started 🚀

We have a thorough guide on how to set up and get started with `viki` in our [documentation](https://github.com/dennislwm/viki/wiki).

## Bugs or Requests 🐛

If you encounter any problems feel free to open an [issue](https://github.com/dennislwm/viki/issues/new?template=bug_report.yml). If you feel the project is missing a feature, please raise a [ticket](https://github.com/dennislwm/viki/issues/new?template=feature_request.yml) on GitHub and I'll look into it. Pull requests are also welcome.

## 📫 How to reach me
<p>
<a href="https://www.linkedin.com/in/dennislwm"><img src="https://img.shields.io/badge/LinkedIn-blue?style=for-the-badge&logo=linkedin&labelColor=blue" height=25></a>
<a href="https://twitter.com/hypowork"><img src="https://img.shields.io/badge/twitter-%231DA1F2.svg?&style=for-the-badge&logo=twitter&logoColor=white" height=25></a>
<a href="https://leetradetitan.medium.com"><img src="https://img.shields.io/badge/medium-%2312100E.svg?&style=for-the-badge&logo=medium&logoColor=white" height=25></a>
<a href="https://dev.to/dennislwm"><img src="https://img.shields.io/badge/DEV.TO-%230A0A0A.svg?&style=for-the-badge&logo=dev-dot-to&logoColor=white" height=25></a>
<a href="https://www.youtube.com/user/dennisleewm"><img src="https://img.shields.io/badge/-YouTube-red?&style=for-the-badge&logo=youtube&logoColor=white" height=25></a>
</p>
<p>
<span class="badge-buymeacoffee"><a href="https://ko-fi.com/dennislwm" title="Donate to this project using Buy Me A Coffee"><img src="https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg" alt="Buy Me A Coffee donate button" /></a></span>
<span class="badge-patreon"><a href="https://patreon.com/dennislwm" title="Donate to this project using Patreon"><img src="https://img.shields.io/badge/patreon-donate-yellow.svg" alt="Patreon donate button" /></a></span>
<span class="badge-newsletter"><a href="https://buttondown.email/dennislwm" title="Subscribe to Newsletter"><img src="https://img.shields.io/badge/newsletter-subscribe-blue.svg" alt="Subscribe Dennis Lee's Newsletter" /></a></span>

