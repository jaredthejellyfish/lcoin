<div id="top"></div>

[![Contributors][contributors-shield]][contributors-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
![Uptime Robot][uptime-shield]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/jarredthejellyfish/lcoin-wallet/raw/main/lcoin_wallet/static/images/l-coin-logo.png">
    <img src="https://github.com/jarredthejellyfish/lcoin-wallet/raw/main/lcoin_wallet/static/images/l-coin-logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">LCoin Wallet</h3>

  <p align="center">
    Currency system written in Python
    <br />
    <a href="https://demo.lcoin.es/">View Demo</a>
    ·
    <a href="https://github.com/jarredthejellyfish/lcoin-wallet/issues">Report Bug</a>
    ·
    <a href="https://github.com/jarredthejellyfish/lcoin-wallet/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Running Locally</a>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>


<br>

<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [![Home Screen Shot][home-screenshot]](https://lcoin.es/) -->

After a very miserable trial run of a physical currency for the Learnlife marketplace I identified the need to use a more scalable alternative.
That is why I came up with LearnCoin (LCoin), a scalable centralized currency system written in Python 3, HTML, and JavaScript.

The current system supports:
* Sending coins
* Receiving coins
* Requesting coins
* Account management
    * Setting a profile picture
    * Custom usernames
    * Password resets

Of course, no one currency system will serve all since their needs may be different. So I'll be adding more features in the near future. You may also suggest changes by opening an issue.

Reference <a href="#getting-started" style="color: #f9a241">Running Locally</a> to run a local copy.

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

These are the major frameworks/libraries used to build the project.

* [Python 3](https://www.python.org/)
    * [Flask](https://pypi.org/project/Flask/)
    * [SQLAlchemy](https://pypi.org/project/SQLAlchemy/)
    * [Jinja2](https://pypi.org/project/Jinja2/)
* [Heroku](https://heroku.com/)
* [Gunicorn](https://gunicorn.org/)
* [Bootstrap](https://getbootstrap.com)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started
To get a local copy up and running follow these simple steps.

<br>

### Prerequisites

Install Python >=3.9 and pip 
  ```sh
  brew install python
  ```
Install pwgen to create secret keys and passwords
  ```sh
  brew install pwgen
  ```
### Installation

_Below are the instructions needed to run your own local copy of LCoin._

1. Clone the repo
   ```sh
   git clone https://github.com/jarredthejellyfish/lcoin-wallet
   ```
<br>

2. Create a `config.ini` file inside the `lcoin_wallet` folder
   ```sh
   touch lcoin_wallet/config.ini
   ```
<br>

3. Generate a random hash to be used as a secret key in Flask
   ```sh
   pwgen 64
   ```
<br>

4. Get an application specific password for your gooogle account *(For Gmail users only)*
    - Navigate to: https://myaccount.google.com/security 
    - Select `App passwords`
    - On `Select app` select `Mail`
    - On `Select device` select `Other`
    - Tap `Generate` and you should be done

<br>

5. Enter the following details in `config.ini` _(replace values in quotes with your own)_
   ```ini
    [SERVER]
    SECRET_KEY = "secret key"
    DATABASE_URI = "database uri"

    [EMAIL]
    EMAIL_USER = "email user"
    EMAIL_PASS = "email password"
   ```

<br>

6. To start the program run:
   ```sh
   python3 run.py
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

This project can serve as a starting point for the building of centralised micro currency systems at a small scale. Or simply as a good kickoff to learn some Flask, Python, and database handling.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap
- [X] Add 500 Error (Internal Server Error) page
- [ ] Add QR code for transactions
- [ ] Add Additional information on transactions
- [ ] Add "Transactions" page to easily see your transactions in one single place
- [ ] Multi-language Support
    - [ ] Catalan
    - [ ] Spanish

See the [open issues](https://github.com/jarredthejellyfish/lcoin-wallet/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Gerard Almenara Hernandez - [@jaredthejellyfish](https://www.instagram.com/jaredthejellyfish/) - ger.almenara@gmail.com

Project Link: [https://github.com/jarredthejellyfish/lcoin-wallet](https://github.com/jarredthejellyfish/lcoin-wallet)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Choose an Open Source License](https://choosealicense.com)
* [Corey Schafer](https://www.youtube.com/c/Coreyms)
* [Img Shields](https://shields.io)
* [Font Awesome](https://fontawesome.com)
* [React Icons](https://react-icons.github.io/react-icons/search)
* [Stormur Bjorn](https://github.com/strumberr)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/jarredthejellyfish/lcoin-wallet?style=for-the-badge
[contributors-url]: https://github.com/jarredthejellyfish/lcoin-wallet/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/jarredthejellyfish/lcoin-wallet?style=for-the-badge
[forks-url]: https://github.com/jarredthejellyfish/lcoin-wallet/network/members

[stars-shield]: https://img.shields.io/github/stars/jarredthejellyfish/lcoin-wallet?style=for-the-badge
[stars-url]: https://github.com/jarredthejellyfish/lcoin-wallet/stargazers

[issues-shield]: https://img.shields.io/github/issues/jarredthejellyfish/lcoin-wallet?style=for-the-badge
[issues-url]: https://github.com/jarredthejellyfish/lcoin-wallet/issues

[license-shield]: https://img.shields.io/github/license/jarredthejellyfish/lcoin-wallet?style=for-the-badge
[license-url]: https://github.com/jarredthejellyfish/lcoin-wallet/blob/master/LICENSE.txt

[uptime-shield]: https://img.shields.io/uptimerobot/ratio/7/m791198016-59e412829242a3b8a5cf9fd3?style=for-the-badge

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/gerard-almenara/

[home-screenshot]: lcoin_wallet/static/images/l-coin-logo.png
